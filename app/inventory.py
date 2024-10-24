# app/inventory.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.seller_products import SellerProduct  # Ensure this model exists
from app.models.category import Category  # Ensure this model exists
from datetime import datetime

bp = Blueprint('seller', __name__, url_prefix='/seller')

@bp.route('/inventory', methods=['GET', 'POST'])
@login_required
def inventory():
    if request.method == 'POST':
        # Update inventory based on form data
        product_ids = request.form.getlist('product_id')
        quantities = request.form.getlist('quantity')

        # Iterate over the products and update quantities
        for product_id, quantity in zip(product_ids, quantities):
            try:
                quantity = int(quantity)
                product_id = int(product_id)
                inventory = Inventory.get_by_product_and_seller(product_id, current_user.id)
                if inventory:
                    Inventory.update_quantity(inventory.inventory_id, quantity)
                else:
                    # Create inventory record if it doesn't exist
                    Inventory.create_inventory(current_user.id, product_id, quantity)
            except ValueError:
                flash(f'Invalid quantity for product ID {product_id}', 'danger')
                continue

        flash('Inventory updated successfully!', 'success')
        return redirect(url_for('seller.inventory'))

    # GET request - display inventory
    # Get the seller's products
    products = Product.get_by_seller(current_user.id)

    # Get inventory for the seller
    inventory_list = Inventory.get_by_seller(current_user.id)
    inventory_dict = {inv.product_id: inv for inv in inventory_list}

    return render_template('seller_profile.html', title='Seller Inventory Data', products=products, inventory=inventory_dict)

@bp.route('/create_product', methods=['GET', 'POST'])
@login_required
def create_product():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        summary = request.form.get('summary')
        price = request.form.get('price')
        category_id = request.form.get('category_id')
        image_url = request.form.get('image_url')
        quantity = request.form.get('quantity')

        # Validate required fields
        if not name or not price or not category_id or not quantity:
            flash('Please fill out all required fields.', 'danger')
            return redirect(url_for('seller.create_product'))

        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            flash('Invalid input for price or quantity.', 'danger')
            return redirect(url_for('seller.create_product'))

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
            # Associate the product with the seller
            SellerProduct.add_seller_product(seller_id=current_user.id, product_id=new_product.product_id)

            # Create initial inventory
            Inventory.create_inventory(
                seller_id=current_user.id,
                product_id=new_product.product_id,
                quantity=quantity
            )

            flash('Product listed successfully!', 'success')
            return redirect(url_for('seller.inventory'))
        else:
            flash('An error occurred while listing the product.', 'danger')
            return redirect(url_for('seller.create_product'))
    else:
        # For GET request, fetch categories to populate dropdown
        categories = Category.get_all()
        return render_template('create_product.html', title='List a New Product', categories=categories)
