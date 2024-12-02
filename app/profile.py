import math
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
import datetime
from decimal import Decimal
from app.models.user import User

from .models.product import Product
from .models.orders import Order  # Updated import
from .models.order_items import OrderItem

from app.models.reviews import Reviews


bp = Blueprint('profile', __name__)

@bp.route('/profile', methods=['GET'])
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
        reviews = Reviews.get_reviews_by_user_id(current_user.id)
    else:
        reviews = None
        orders_with_items = None
        page = None
        total_pages = None

    return render_template(
        'profile.html',
        reviews=reviews,
        orders_with_items=orders_with_items,
        page=page,
        total_pages=total_pages
    )


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


@bp.route('/add-review', methods=['POST'])
def add_review():
    # Parse the JSON payload
    data = request.get_json()

    # Extract required fields from the JSON data
    seller_id = data.get('seller_id')
    product_id = data.get('product_id')
    rating = data.get('rating')
    comment = data.get('comment')

    # Use the authenticated user's ID as reviewer_id
    reviewer_id = data.get('reviewer_id')  # Or use current_user.id if authenticated
    
    
    # TODO: Add validation and customer authentication

    # Create the review
    success = Reviews.create_review(
        seller_id=seller_id,
        reviewer_id=reviewer_id,
        product_id=product_id,
        rating=rating,
        comment=comment
    )

    if success:
        return jsonify({'message': 'Review added successfully.'}), 201
    else:
        return jsonify({'error': 'Failed to add review.'}), 500