import math
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
import datetime
from decimal import Decimal
from app.models.user import User

from .models.product import Product
from .models.orders import Order  # Updated import
from .models.order_items import OrderItem

from .models.reviews import Reviews


bp = Blueprint('profile', __name__)

@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    if current_user.is_authenticated:
        # Get page number from request args
        page = request.args.get('page', 1, type=int)
        per_page = 4  # Show 4 orders per page

        # Get all orders for the user
        all_orders = Order.get_by_user(current_user.id)

        # Compute total pages
        total_orders = len(all_orders)
        total_pages = math.ceil(total_orders / per_page)

        # Slice orders for current page
        start = (page - 1) * per_page
        end = start + per_page
        orders = all_orders[start:end]

        # For each order, get the associated order items and product details
        orders_with_items = []
        for order in orders:
            order_items = OrderItem.get_by_order(order.order_id)
            items_with_details = []
            for item in order_items:
                product = Product.get(item.product_id)
                items_with_details.append({
                    'order_item': item,
                    'product': product
                })
            orders_with_items.append({
                'order': order,
                'items': items_with_details
            })
        # Get recent reviews
        reviews = Reviews.get_reviews_by_user_id(current_user.user_id)
        print(reviews)
        print(current_user.id)
    else:
        reviews = None
        orders_with_items = None
        page = None
        total_pages = None

    # Fetch seller's products and associated reviews
    seller_products = []
    product_reviews = []
    if current_user.is_seller:
        seller_products = Product.get_by_seller(current_user.user_id)
        for product in seller_products:
            reviews = Reviews.get_by_product(product.product_id)
            product_reviews.append({
                'product': product,
                'reviews': reviews
            })

    return render_template(
        'profile.html',
        reviews=reviews,
        orders_with_items=orders_with_items,
        page=page,
        total_pages=total_pages,
        seller_products=seller_products,
        product_reviews=product_reviews
    )
@bp.route('/profile/toggle_to_seller', methods=['POST'])
@login_required
def toggle_to_seller():
    current_user.toggle_to_seller()
    flash('You are now a seller!', 'success')
    return redirect(url_for('profile.profile'))

@bp.route('/profile/update', methods=['GET', 'POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        address = request.form.get('address')
        summary = request.form.get('summary')
        password = request.form.get('password')

        # Get balance action and amount
        balance_action = request.form.get('balance_action')
        balance_amount = request.form.get('balance_amount')

        # Validate and update email
        if email != current_user.email and User.email_exists(email):
            flash('Email already in use.', 'danger')
            return render_template(
                'update_profile.html',
                first_name=first_name,
                last_name=last_name,
                email=email,
                address=address,
                summary=summary,
                balance=current_user.balance  # Pass current balance
            )

        # Update email if changed
        if email != current_user.email:
            current_user.change_email(email)

        # Update other attributes
        current_user.update_first_name(first_name)
        current_user.update_last_name(last_name)
        current_user.update_address(address)
        current_user.update_summary(summary)

        # Handle balance update
        if balance_action and balance_amount:
            try:
                amount = Decimal(balance_amount)  # Convert amount to Decimal
                if amount <= 0:
                    raise ValueError("Amount must be positive.")

                if balance_action == 'add':
                    new_balance = current_user.balance + amount
                elif balance_action == 'withdraw':
                    if amount > current_user.balance:
                        flash('You cannot withdraw more than your current balance.', 'danger')
                        return redirect(url_for('profile.update_profile'))
                    new_balance = current_user.balance - amount
                else:
                    flash('Invalid balance action.', 'danger')
                    return redirect(url_for('profile.update_profile'))

                # Update balance
                current_user.update_balance(new_balance)
            except ValueError as e:
                flash(str(e), 'danger')
                return redirect(url_for('profile.update_profile'))

        # Update password if provided
        if password:
            current_user.change_password(password)

        flash('Profile updated successfully.', 'success')
        return redirect(url_for('profile.profile'))
    else:
        return render_template(
            'update_profile.html',
            first_name=current_user.first_name,
            last_name=current_user.last_name,
            email=current_user.email,
            address=current_user.address,
            summary=current_user.summary,
            balance=current_user.balance  # Pass current balance
        )
    
