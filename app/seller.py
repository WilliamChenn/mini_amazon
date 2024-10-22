from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from flask import Blueprint
from datetime import datetime

bp = Blueprint('seller', __name__)

# Sample inventory data with last_modified field
inventory_data = [
    {'name': 'Charizard Blood Elixir', 'price': 540.99, 'quantity': 5, 'last_modified': datetime.now()},
    {'name': 'Master Balls', 'price': 150.99, 'quantity': 2, 'last_modified': datetime.now()},
    {'name': 'Premium Battle Passes', 'price': 799.99, 'quantity': 10, 'last_modified': datetime.now()},
]

@bp.route('/seller/inventory', methods=['GET', 'POST'])
def inventory():
    if request.method == 'POST':
        # Update inventory based on form data
        for i, item in enumerate(inventory_data):
            item_name = request.form.get(f'product_name_{i+1}')
            item_price = request.form.get(f'price_{i+1}')
            item_quantity = request.form.get(f'quantity_{i+1}')

            # Convert price and quantity to their respective types for comparison
            item_price = float(item_price)
            item_quantity = int(item_quantity)

            # Check if any of the fields have changed
            if (item_name != item['name'] or
                item_price != item['price'] or
                item_quantity != item['quantity']):
                
                # Update the item fields and set the new last_modified time
                item['name'] = item_name
                item['price'] = item_price
                item['quantity'] = item_quantity
                item['last_modified'] = datetime.now()

        flash('Inventory updated successfully!')
        return redirect(url_for('seller.inventory'))

    return render_template('seller.html', title='Seller Inventory', inventory=inventory_data)
