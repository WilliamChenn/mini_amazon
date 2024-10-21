from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user

from app.models.reviews import Reviews


bp = Blueprint('social', __name__)

@bp.route('/profile', methods=['GET'])
def recent_reviews():
    
    if current_user.is_authenticated:
        reviews = Reviews.get_top_by_user_id(current_user.id)
    else:
        reviews = None
    
    return render_template('profile.html', reviews=reviews)

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