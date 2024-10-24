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
    
    @staticmethod
    def get_by_product_and_seller(product_id, seller_id):
        row = app.db.execute('''
SELECT inventory_id, seller_id, product_id, quantity, updated_at
FROM Inventory
WHERE product_id = :product_id AND seller_id = :seller_id
LIMIT 1
''', product_id=product_id, seller_id=seller_id)
        return Inventory(*row) if row else None
    
    @staticmethod
    def get_by_product_id(product_id):
        rows = app.db.execute('''
            SELECT inventory_id, seller_id, product_id, quantity, updated_at
            FROM Inventory
            WHERE product_id = :product_id
        ''', product_id=product_id)
        return Inventory(*rows[0]) if rows else None

    @staticmethod
    def update_quantity(inventory_id, new_quantity):
        try:
            app.db.execute('''
                UPDATE Inventory
                SET quantity = :quantity, updated_at = CURRENT_TIMESTAMP
                WHERE inventory_id = :inventory_id
            ''', quantity=new_quantity, inventory_id=inventory_id)
            return True
        except Exception as e:
            app.logger.error(f"Error updating inventory {inventory_id}: {e}")
            return False

    @staticmethod
    def create_inventory(seller_id, product_id, quantity):
        try:
            rows = app.db.execute('''
                INSERT INTO Inventory (seller_id, product_id, quantity)
                VALUES (:seller_id, :product_id, :quantity)
                RETURNING inventory_id, seller_id, product_id, quantity, updated_at
            ''', seller_id=seller_id, product_id=product_id, quantity=quantity)
            return Inventory(*rows[0]) if rows else None
        except Exception as e:
            app.logger.error(f"Error creating inventory for product {product_id}: {e}")
            return None
