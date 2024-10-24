from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.seller_products import SellerProduct  # Assuming you have this model
from datetime import datetime

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
        # Render the product creation form
        return render_template('create_product.html')
