from flask import current_app as app

class Inventory:
    def __init__(self, inventory_id, seller_id, product_id, quantity, updated_at):
        self.inventory_id = inventory_id
        self.seller_id = seller_id
        self.product_id = product_id
        self.quantity = quantity
        self.updated_at = updated_at

    @staticmethod
    def get_by_seller(seller_id):
        rows = app.db.execute('''
SELECT inventory_id, seller_id, product_id, quantity, updated_at
FROM Inventory
WHERE seller_id = :seller_id
''', seller_id=seller_id)
        return [Inventory(*row) for row in rows]

    @staticmethod
    def get_by_product(product_id):
        rows = app.db.execute('''
SELECT inventory_id, seller_id, product_id, quantity, updated_at
FROM Inventory
WHERE product_id = :product_id
''', product_id=product_id)
        return [Inventory(*row) for row in rows]
