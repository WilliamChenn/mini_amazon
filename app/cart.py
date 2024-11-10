from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app as app
from flask_login import login_required, current_user
from .models.cart import Cart
from .models.cart_items import CartItem
from .models.product import Product
from .models.user import User
from .models.orders import Order
from .models.order_items import OrderItem
from .models.inventory import Inventory

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
    product = Product.get(product_id)
    if not product or not product.available:
        flash('Product not available.', 'danger')
        return redirect(url_for('index.index'))

    # Get data from form
    try:
        quantity = int(request.form.get('quantity', 1))
        seller_id = int(request.form.get('seller_id'))
        if quantity < 1:
            raise ValueError
    except (ValueError, TypeError):
        flash('Invalid input.', 'danger')
        return redirect(url_for('products.product_page', product_id=product_id))

    # Check inventory
    inventory = Inventory.get_by_product_and_seller(product_id, seller_id)
    if not inventory:
        flash('Seller does not have this product.', 'danger')
        return redirect(url_for('products.product_page', product_id=product_id))

    if inventory.quantity < quantity:
        flash(f'Requested quantity exceeds available inventory ({inventory.quantity}).', 'danger')
        return redirect(url_for('products.product_page', product_id=product_id))

    cart = Cart.get_or_create_cart(current_user.user_id)
    CartItem.add_to_cart(
        cart_id=cart.cart_id,
        product_id=product.product_id,
        seller_id=seller_id,
        quantity=quantity
    )

    flash(f'Added {quantity} x {product.name} to your cart.', 'success')
    return redirect(url_for('cart.view_cart'))

@bp.route('/remove/<int:cart_item_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_item_id):
    # Retrieve the user's cart
    cart = Cart.get_or_create_cart(current_user.user_id)
    # Fetch the specific cart item by ID
    # Remove the item from the database
    success = CartItem.remove_from_cart(cart_item_id)
    if success:
        flash(f'Item removed from your cart.', 'success')
    else:
        flash(f'Failed to remove item from your cart.', 'danger')
    return redirect(url_for('cart.view_cart'))


@bp.route('/update/<int:cart_item_id>', methods=['POST'])
@login_required
def update_cart_item(cart_item_id):
    # Get the new quantity from the form
    try:
        new_quantity = int(request.form.get('quantity', 1))
        if new_quantity < 1:
            raise ValueError
    except ValueError:
        flash('Invalid quantity.', 'danger')
        return redirect(url_for('cart.view_cart'))

    # Update the cart item
    CartItem.update_quantity(cart_item_id=cart_item_id, quantity=new_quantity)

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

@bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    try:
        cart = Cart.get_or_create_cart(current_user.user_id)
        cart_items = CartItem.get_cart_items(cart.cart_id)
        if not cart_items:
            flash('Your cart is empty.', 'warning')
            return redirect(url_for('cart.view_cart'))
    except Exception as e:
        flash(f'Error retrieving cart or cart items: {str(e)}', 'danger')
        return redirect(url_for('cart.view_cart'))
    
    try:
        total_amount = 0
        num_items = 0
        order_items_data = []
        
        for item in cart_items:
            try:
                product = Product.get(item.product_id)
                if not product or not product.available:
                    flash(f'Product "{product.name}" is not available for purchase.', 'warning')
                    return redirect(url_for('cart.view_cart'))
                
                inventory = Inventory.get_by_product_and_seller(item.product_id, item.seller_id)
                if not inventory or inventory.quantity < item.quantity:
                    flash(f'Insufficient inventory for "{product.name}".', 'danger')
                    return redirect(url_for('cart.view_cart'))
                
                total_amount += product.price * item.quantity
                num_items += item.quantity
                order_items_data.append({
                    'product_id': product.product_id,
                    'seller_id': item.seller_id,
                    'quantity': item.quantity,
                    'unit_price': product.price,
                    'total_price': product.price * item.quantity
                })
            except Exception as e:
                flash(f'Error processing item {item.product_id}: {str(e)}', 'danger')
                return redirect(url_for('cart.view_cart'))
        
        # Check buyer's balance
        new_buyer_balance = current_user.balance - total_amount
        if new_buyer_balance < 0:
            flash('Insufficient balance.', 'danger')
            return redirect(url_for('cart.view_cart'))
        
        # Create Order
        order = Order.create(
            user_id=current_user.user_id,
            total_amount=total_amount,
            num_items=num_items,
            fulfillment_status='Pending'
        )
        if not order:
            flash('Failed to create order.', 'danger')
            return redirect(url_for('cart.view_cart'))
        
        # Create OrderItems and Update Inventory & Seller Balances
        for item_data in order_items_data:
            order_item = OrderItem.create(**item_data, order_id=order.order_id)
            if not order_item:
                flash(f'Failed to create order item for product ID: {item_data["product_id"]}', 'danger')
                return redirect(url_for('cart.view_cart'))
            
            # Decrement Inventory
            Inventory.update_quantity(
                inventory_id=Inventory.get_by_product_and_seller(
                    item_data['product_id'], item_data['seller_id']
                ).inventory_id,
                new_quantity=Inventory.get_by_product_and_seller(
                    item_data['product_id'], item_data['seller_id']
                ).quantity - item_data['quantity']
            )
        
       # Deduct Total Amount from Buyer's Balance
        current_user.update_balance(new_balance=new_buyer_balance)
        
        # Clear Cart
        CartItem.clear_cart(cart.cart_id)
        
    except Exception as e:
        app.logger.error(f"Checkout Error: {e}")
        flash(f'An error occurred during checkout: {str(e)}', 'danger')
        return redirect(url_for('cart.view_cart'))
    
    flash('Checkout successful!', 'success')
    return redirect(url_for('cart.view_cart'))