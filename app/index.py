from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.orders import Order
from .models.order_items import OrderItem
from .models.inventory import Inventory

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    # Get all available products for sale
    products = Product.get_all(True)
    
    # Compute total quantities for each product
    product_quantities = {}
    for product in products:
        inventory_list = Inventory.get_by_product(product.product_id)
        total_quantity = sum(inv.quantity for inv in inventory_list)
        product_quantities[product.product_id] = total_quantity

    # Find the orders current user has made since a specific date
    if current_user.is_authenticated:
        since_date = datetime.datetime(1980, 9, 14)
        orders = Order.get_all_by_uid_since(current_user.user_id, since_date)
    else:
        orders = None

    # Pass the data to the template
    return render_template(
        'index.html',
        avail_products=products,
        order_history=orders,
        product_quantities=product_quantities
    )