from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_login import login_required, current_user
from .models.purchase import Purchase
from .models.product import Product

bp = Blueprint('purchase', __name__, url_prefix='/purchase')

@bp.route('/checkout')
@login_required
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty.')
        return redirect(url_for('cart.view_cart'))
    
    total = 0
    for product_id, quantity in cart.items():
        product = Product.get_by_id(int(product_id))
        if product:
            total += product.price * quantity
            # Here you would typically create a Purchase record
            Purchase.create(user_id=current_user.id, product_id=product.id, quantity=quantity)
    
    # Clear the cart after checkout
    session['cart'] = {}
    flash(f'Checkout successful! Total amount: ${total:.2f}')
    return redirect(url_for('index.index'))
