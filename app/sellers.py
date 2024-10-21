# app/sellers.py

from flask import Blueprint, render_template, flash, redirect, url_for
from .models.inventory import Inventory
from .models.product import Product
from .models.user import User

bp = Blueprint('sellers', __name__, url_prefix='/seller')

@bp.route('/<int:seller_id>/inventory')
def view_inventory(seller_id):
    # Retrieve seller details
    seller = User.get_by_id(seller_id)
    if not seller or not seller.is_seller:
        flash('Seller not found or is not a valid seller.', 'danger')
        return redirect(url_for('index.index'))

    # Retrieve inventory items
    inventory_items = Inventory.get_inventory_by_seller(seller_id)
    if not inventory_items:
        flash('This seller has no products in their inventory.', 'info')
        return render_template('seller_inventory.html', seller=seller, products=[])

    # Gather product details
    products = []
    for item in inventory_items:
        product = Product.get(item.product_id)
        if product:
            products.append({
                'product': product,
                'quantity': item.quantity,
                'inventory_item_id': item.inventory_id
            })

    return render_template('seller_inventory.html', seller=seller, products=products)
