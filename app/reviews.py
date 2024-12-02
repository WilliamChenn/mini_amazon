from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import delete

from app.models.product import Product
from app.models.reviews import Reviews
from app.models.user import User


bp = Blueprint('reviews', __name__)

@bp.route('/add-review/<int:product_id>/<int:seller_id>', methods=['GET', 'POST'])
def add_review(product_id, seller_id):
    
    if request.method == 'POST':
        # Retrieve form data
        rating = request.form.get('rating')
        comment = request.form.get('comment')

        # Validate and save the review (mock logic)
        if not (rating and comment):
            flash('All fields are required.', 'danger')
            return redirect(url_for('review.add_review', product_id=product_id))

        # Check if user has already reviewed the product
        if(Reviews.review_user_id_exists(current_user.id, product_id)):
            flash('You have already reviewed this product!', 'danger')
            return redirect(url_for('products.product_page', product_id=product_id))
        
        # Create review
        Reviews.create_review(seller_id, current_user.id, product_id, rating, comment)
        flash('Review added successfully!', 'success')
        return redirect(url_for('products.product_page', product_id=product_id))
    
    print(seller_id)
    # On GET, render the form
    product = Product.get(product_id)
    return render_template('add_review.html', form_data={}, product_id=product_id,  product_name=product.name, seller_id=seller_id)

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

@bp.route('/delete-review/<int:review_id>/<int:product_id>', methods=['GET'])
def delete_review(review_id, product_id):
    
    review = Reviews.delete_review(review_id)
    flash('Review deleted successfully!', 'success')
    return redirect(url_for('products.product_page', product_id=product_id))
