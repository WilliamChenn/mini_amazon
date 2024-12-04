from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import delete
from app.models.orders import Order

from app.models.product import Product
from app.models.reviews import Reviews
from app.models.user import User


bp = Blueprint('reviews', __name__)

@bp.route('/add-review-product/<int:product_id>', methods=['GET', 'POST'])
def add_review_product(product_id):
    
    if request.method == 'POST':
        # Retrieve form data
        rating = request.form.get('rating')
        comment = request.form.get('comment')

        # Validate and save the review (mock logic)
        if not (rating and comment):
            flash('All fields are required.', 'danger')
            return redirect(url_for('review.add_review', product_id=product_id))

        # Check if user has already reviewed the product or user has not purchased product
        if(Reviews.review_user_id_exists(current_user.id, product_id)):
            flash('You have already reviewed this product!', 'danger')
            return redirect(url_for('products.product_page', product_id=product_id))
        
        if not Order.get_order_by_user_id(current_user.id, product_id):
            flash('You have not bought this product yet!', 'danger')
            return redirect(url_for('products.product_page', product_id=product_id))
    
        # Create review
        Reviews.create_review(None, current_user.id, product_id, rating, comment, True)
        flash('Review added successfully!', 'success')
        return redirect(url_for('products.product_page', product_id=product_id))
    
    # On GET, render the form
    product = Product.get(product_id)
    return render_template('add_review.html', form_data={}, product_id=product_id,  product_name=product.name, seller_id=seller_id)

@bp.route('/add-review-seller/<int:seller_id>', methods=['GET', 'POST'])
def add_review_seller(seller_id):
    
    if request.method == 'POST':
        # Retrieve form data
        rating = request.form.get('rating')
        comment = request.form.get('comment')

        # Validate and save the review (mock logic)
        if not (rating and comment):
            flash('All fields are required.', 'danger')
            return redirect(url_for('review.add_review_seller', seller_id=seller_id))

        # Check if user has already reviewed the product or user has not purchased product
        if(Reviews.review_seller_user_id_exists(current_user.id, seller_id)):
            flash('You have already reviewed this seller!', 'danger')
            return redirect(url_for('users.public_profile', user_id=seller_id))
        
        if not Order.get_order_by_user_id_seller(current_user.id, seller_id):
            flash('You have not bought from this seller yet!', 'danger')
            return redirect(url_for('users.public_profile', user_id=seller_id))
    
        # Create review
        Reviews.create_review(seller_id, current_user.id, None, rating, comment, False)
        flash('Review added successfully!', 'success')
        return redirect(url_for('users.public_profile', user_id=seller_id))
    
    # On GET, render the form
    user = User.get(seller_id)
    return render_template('add_review_seller.html', form_data={}, user_id=user.user_id, first_name=user.first_name, seller_id=seller_id)

@bp.route('/edit-review/<int:review_id>/<int:product_id>', methods=['GET', 'POST'])
def edit_review(review_id, product_id):
    
    if request.method == 'POST':
        # Retrieve form data
        rating = request.form.get('rating')
        comment = request.form.get('comment')

        # Validate and save the review (mock logic)
        if not (rating and comment):
            flash('All fields are required.', 'danger')
            return redirect(url_for('review.edit_review', review_id=review_id, product_id = product_id))
        
        # Update review
        Reviews.update_review(review_id, rating, comment)
        flash('Review added successfully!', 'success')
        return redirect(url_for('products.product_page', product_id=product_id))

    # On GET, render the form
    review = Reviews.get_by_id(review_id)
    product = Product.get(product_id)
    return render_template('edit_review.html', form_data={}, review=review, product=product)

@bp.route('/edit-review-seller/<int:review_id>/<int:seller_id>', methods=['GET', 'POST'])
def edit_review_seller(review_id, seller_id):
    
    if request.method == 'POST':
        # Retrieve form data
        rating = request.form.get('rating')
        comment = request.form.get('comment')

        # Validate and save the review (mock logic)
        if not (rating and comment):
            flash('All fields are required.', 'danger')
            return redirect(url_for('review.edit_review_seller', review_id=review_id, seller_id = seller_id))
        
        # Update review
        Reviews.update_review(review_id, rating, comment)
        flash('Review added successfully!', 'success')
        return redirect(url_for('users.public_profile', user_id=seller_id))

    # On GET, render the form
    review = Reviews.get_by_id(review_id)
    user = User.get(seller_id)
    return render_template('edit_review_seller.html', form_data={}, review=review, user=user)

@bp.route('/delete-review/<int:review_id>/<int:product_id>', methods=['GET'])
def delete_review(review_id, product_id):
    
    review = Reviews.delete_review(review_id)
    flash('Review deleted successfully!', 'success')
    return redirect(url_for('products.product_page', product_id=product_id))

@bp.route('/delete-review-seller/<int:review_id>/<int:seller_id>', methods=['GET'])
def delete_review_seller(review_id, seller_id):
    
    review = Reviews.delete_review(review_id)
    flash('Review deleted successfully!', 'success')
    return redirect(url_for('users.public_profile', user_id=seller_id))

@bp.route('/view-reviews/', methods=['GET'])
def view_reviews():
    
    seller_reviews = Reviews.get_seller_reviews()
    product_reviews = Reviews.get_product_reviews()
    
    # Combine the results and add a "type" field for distinction
    all_reviews = [
        {**review, 'type': 'seller'} for review in seller_reviews
    ] + [
        {**review, 'type': 'product'} for review in product_reviews
    ]

    # Sort the combined reviews by rating (descending), then date (descending)
    sorted_reviews = sorted(
        all_reviews,
        key=lambda x: (-x['average_rating'], x['latest_review_date'])
    )
    
    return render_template('view_reviews.html', reviews=sorted_reviews)