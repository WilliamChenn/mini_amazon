from flask import current_app as app, Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.seller_products import SellerProduct  # Assuming you have this model
from datetime import datetime
from app.models.reviews import Reviews
from app.models.user import User  # Import the User model
from app.models.category import Category  # Import the Category model

bp = Blueprint('products', __name__, url_prefix='/products')

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_product():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        summary = request.form.get('summary')
        price = request.form.get('price')
        category_id = request.form.get('category_id')
        image_url = request.form.get('image_url')
        quantity = request.form.get('quantity')
        # Check if the product already exists for this seller
        if Product.exists_for_seller(name, current_user.id):
            flash('Item already exists', 'danger')
            return redirect(url_for('products.create_product'))
        # Validate form data
        if not name or not price or not category_id or not quantity:
            flash('Please fill out all required fields.')
            return redirect(url_for('products.create_product'))

        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            flash('Invalid price or quantity.')
            return redirect(url_for('products.create_product'))
        # Create the product
        new_product = Product.create(
            seller_id=current_user.id,
            category_id=category_id,
            name=name,
            summary=summary,
            image_url=image_url,
            price=price,
            available=True
        )

        if new_product:
            # Add product to seller_products table
            SellerProduct.add_seller_product(seller_id=current_user.id, product_id=new_product.product_id)

            # Create inventory record
            Inventory.create_inventory(
                seller_id=current_user.id,
                product_id=new_product.product_id,
                quantity=quantity
            )

            flash('Product created successfully!')
            return redirect(url_for('seller.create_product'))
        else:
            flash('An error occurred while creating the product.')
            return redirect(url_for('products.create_product'))
    else:
        # For GET request, fetch categories
        categories = Category.get_all()
        form_data = {}  # Initialize form_data as an empty dictionary
        return render_template('create_product.html', categories=categories, form_data=form_data)

@bp.route('/<int:product_id>')
def product_page(product_id):
    product = Product.get(product_id)
    if not product:
        flash('Product not found.', 'danger')
        return redirect(url_for('index.index'))

    # Get category information
    category = Category.get(product.category_id)

    # Get sellers with inventory for the product
    inventory = Inventory.get_by_product(product_id)
    sellers = []
    for inv in inventory:
        seller = User.get(inv.seller_id)
        if inv.quantity > 0 and seller:
            sellers.append({
                'seller': seller,
                'quantity': inv.quantity
            })

    # Get reviews for the product
    reviews = Reviews.get_by_product(product_id)
    average_rating = None
    if reviews:
        average_rating = sum(review.rating for review in reviews) / len(reviews)

        # Fetch reviewer information and attach to each review
        for review in reviews:
            reviewer = User.get(review.reviewer_id)
            review.reviewer = reviewer  # Attach reviewer to review

    return render_template(
        'product.html',
        product=product,
        reviews=reviews,
        average_rating=average_rating,
        sellers=sellers,
        category=category
    )

@bp.route('/autocomplete')
def autocomplete():
    search = request.args.get('q', '')
    product_names = Product.get_product_names(search)
    return jsonify(matching_results=product_names)

# FILE: app/models/product.py

@staticmethod
def search_by_name(search_query):
    rows = app.db.execute(
        '''
        SELECT product_id, seller_id, category_id, name, summary, image_url, price, created_at, updated_at, available
        FROM Products
        WHERE LOWER(name) LIKE LOWER(:search_query)
        ''',
        search_query=f'%{search_query}%'
    )
    return [Product(*row) for row in rows]
