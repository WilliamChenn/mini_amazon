from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .models.cart import Cart
from .models.cart_items import CartItem
from .models.product import Product

bp = Blueprint('cart', __name__, url_prefix='/cart')

@bp.route('/')
@login_required
def view_cart():
    # Retrieve or create the user's cart
    cart = Cart.get_or_create_cart(current_user.user_id)
    cart_items = CartItem.get_cart_items(cart.cart_id)

    # Retrieve product details and calculate total
    products = []
    total = 0
    for item in cart_items:
        product = Product.get(item.product_id)
        if product:
            subtotal = product.price * item.quantity
            total += subtotal
            products.append({
                'cart_item': item,
                'product': product,
                'subtotal': subtotal
            })

    return render_template('cart.html', products=products, total=total)

@bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    # Retrieve the product details
    product = Product.get(product_id)
    if not product or not product.available:
        flash('Product not available.', 'danger')
        return redirect(url_for('index.index'))

    # Retrieve or create the user's cart
    cart = Cart.get_or_create_cart(current_user.user_id)

    # Add to cart (handles updating quantity if item exists)
    cart_item = CartItem.add_to_cart(
        cart_id=cart.cart_id,
        product_id=product.product_id,
        seller_id=product.seller_id,
        quantity=1  # You can modify this to accept quantity from the form
    )

    flash(f'Added {product.name} to your cart.', 'success')
    return redirect(url_for('cart.view_cart'))

@bp.route('/remove/<int:cart_item_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_item_id):
    # Retrieve the cart item to ensure it belongs to the current user
    cart = Cart.get_or_create_cart(current_user.user_id)
    cart_item = None
    for item in CartItem.get_cart_items(cart.cart_id):
        if item.cart_item_id == cart_item_id:
            cart_item = item
            break

    if not cart_item:
        flash('Cart item not found.', 'danger')
        return redirect(url_for('cart.view_cart'))

    # Remove the item from the cart
    CartItem.remove_from_cart(cart_item_id)
    flash('Item removed from your cart.', 'success')
    return redirect(url_for('cart.view_cart'))

@bp.route('/update/<int:cart_item_id>', methods=['POST'])
@login_required
def update_cart_item(cart_item_id):
    # Retrieve the cart item to ensure it belongs to the current user
    cart = Cart.get_or_create_cart(current_user.user_id)
    cart_item = None
    for item in CartItem.get_cart_items(cart.cart_id):
        if item.cart_item_id == cart_item_id:
            cart_item = item
            break

    if not cart_item:
        flash('Cart item not found.', 'danger')
        return redirect(url_for('cart.view_cart'))

    # Get the new quantity from the form
    try:
        new_quantity = int(request.form.get('quantity', 1))
        if new_quantity < 1:
            raise ValueError
    except ValueError:
        flash('Invalid quantity.', 'danger')
        return redirect(url_for('cart.view_cart'))

    # Update the cart item
    app.db.execute('''
        UPDATE Cart_items
        SET quantity = :quantity, added_at = CURRENT_TIMESTAMP
        WHERE cart_item_id = :cart_item_id
    ''', quantity=new_quantity, cart_item_id=cart_item_id)

    flash('Cart updated successfully.', 'success')
    return redirect(url_for('cart.view_cart'))

@bp.route('/clear', methods=['POST'])
@login_required
def clear_cart():
    # Retrieve the user's cart
    cart = Cart.get_or_create_cart(current_user.user_id)

    # Clear all items from the cart
    CartItem.clear_cart(cart.cart_id)

    flash('All items have been removed from your cart.', 'success')
    return redirect(url_for('cart.view_cart'))
