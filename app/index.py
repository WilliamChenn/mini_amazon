from flask import render_template, request
from flask_login import current_user
import datetime
import math

from .models.product import Product
from .models.orders import Order
from .models.order_items import OrderItem
from .models.inventory import Inventory
from app.models.category import Category
from .models.reviews import Reviews
from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/', methods=['GET'])
def index():
    # Fetch all categories
    categories_list = Category.get_all()

    # Build a mapping from category_id to category
    categories_dict = {category.category_id: category for category in categories_list}

    # Initialize an empty dictionary to hold the tree
    category_tree = {}

    # Build the tree structure
    for category in categories_list:
        category.children = []  # Initialize children list

    for category in categories_list:
        if category.parent_id is not None:
            parent = categories_dict.get(category.parent_id)
            if parent:
                parent.children.append(category)
        else:
            category_tree[category.category_id] = category

    # Now category_tree contains top-level categories with nested children
    # Rest of your existing code...

    # Example: Fetch products, handle search queries, etc.
    # Get category filter
    category_id = request.args.get('category_id', type=int)
    search_query = request.args.get('search_query', '')
    
    # Get products filtered by category and search
    products = Product.search(search_query, category_id)
    
    # Compute total quantities for each product
    product_quantities = {}
    for product in products:
        inventory_list = Inventory.get_by_product(product.product_id)
        total_quantity = sum(inv.quantity for inv in inventory_list)
        product_quantities[product.product_id] = total_quantity

    # Calculate average rating for each product
    for product in products:
        reviews = Reviews.get_by_product(product.product_id)
        if reviews:
            product.average_rating = sum(review.rating for review in reviews) / len(reviews)
        else:
            product.average_rating = None

    # Pagination setup
    page = request.args.get('page', 1, type=int)
    per_page = 12
    total_products = len(products)
    total_pages = math.ceil(total_products / per_page)

    # Slice products for current page
    start = (page - 1) * per_page
    end = start + per_page
    paginated_products = products[start:end]

    # Find the orders current user has made since a specific date
    if current_user.is_authenticated:
        since_date = datetime.datetime(1980, 9, 14)
        orders = Order.get_all_by_uid_since(current_user.user_id, since_date)
    else:
        orders = None

    # Pass the data to the template
    return render_template(
        'index.html',
        avail_products=paginated_products,
        order_history=orders,
        product_quantities=product_quantities,
        categories=category_tree,
        page=page,
        total_pages=total_pages,
        current_category_id=category_id
    )