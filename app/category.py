from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import current_user, login_required
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.seller_products import SellerProduct  # Assuming you have this model
from datetime import datetime
from app.models.reviews import Reviews
from app.models.user import User  # Import the User model
from app.models.category import Category  # Import the Category model

# Define the blueprint with the name 'categories'
bp = Blueprint('categories', __name__, url_prefix='/categories')

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_category():
    if request.method == 'POST':
        category_name = request.form.get('category_name')
        parent_id = request.form.get('parent_id') or None

        # Retrieve existing form data from hidden fields
        form_data = {
            'name': request.form.get('product_name'),
            'summary': request.form.get('summary'),
            'price': request.form.get('price'),
            'quantity': request.form.get('quantity'),
            'image_url': request.form.get('image_url'),
        }

        if category_name:
            new_category = Category.create(category_name, parent_id)
            if new_category:
                flash('Category created successfully!', 'success')
                # Store the form data in the session
                session['create_product_form_data'] = form_data
                return redirect(url_for('seller.create_product'))
            else:
                flash('Failed to create category.', 'danger')
        else:
            flash('Category name is required.', 'danger')

    categories = Category.get_all()
    return render_template('create_category.html', categories=categories)

@bp.route('/children')
def get_children():
    parent_id = request.args.get('parent_id', type=int)
    if parent_id is None:
        # Handle the case where parent_id is not provided
        return jsonify([])
    categories = Category.get_children(parent_id)
    return jsonify([{'category_id': c.category_id, 'category_name': c.category_name} for c in categories])