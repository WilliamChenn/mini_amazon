from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
#from .models.purchase import Purchase
from .models.orders import Order  # Updated import
from .models.order_items import OrderItem

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    # Get all available products for sale
    products = Product.get_all(True)
    
    # Find the orders current user has made since a specific date
    if current_user.is_authenticated:
        since_date = datetime.datetime(1980, 9, 14, 0, 0, 0)
        orders = Order.get_all_by_uid_since(current_user.user_id, since_date)
        
    else:
        orders = None
    
    # Render the page by adding information to the index.html file
    return render_template('index.html',
                       avail_products=products,
                       order_history=orders)  # Changed to 'order_history'