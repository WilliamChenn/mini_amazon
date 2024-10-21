from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user
import datetime

from .models.product import Product
#from .models.purchase import Purchase
from .models.orders import Order  # Updated import
from .models.order_items import OrderItem

from app.models.reviews import Reviews


bp = Blueprint('profile', __name__)

@bp.route('/profile', methods=['GET'])
def profile():
    if current_user.is_authenticated:
        # Get recent reviews
        reviews = Reviews.get_top_by_user_id(current_user.id)
        
        # Get the user's orders
        orders = Order.get_by_user(current_user.id)
        
        # For each order, get the associated order items and product details
        orders_with_items = []
        for order in orders:
            order_items = OrderItem.get_by_order(order.order_id)
            # For each order item, get product details
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
    else:
        reviews = None
        orders_with_items = None

    return render_template('profile.html', reviews=reviews, orders_with_items=orders_with_items)





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