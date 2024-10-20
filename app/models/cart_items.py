from flask import current_app as app

class CartItem:
    def __init__(self, cart_item_id, cart_id, product_id, seller_id, quantity, added_at):
        self.cart_item_id = cart_item_id
        self.cart_id = cart_id
        self.product_id = product_id
        self.seller_id = seller_id
        self.quantity = quantity
        self.added_at = added_at

    @staticmethod
    def get_cart_items(cart_id):
        rows = app.db.execute('''
SELECT cart_item_id, cart_id, product_id, seller_id, quantity, added_at
FROM Cart_items
WHERE cart_id = :cart_id
''', cart_id=cart_id)
        return [CartItem(*row) for row in rows] if rows else []

    @staticmethod
    def add_to_cart(cart_id, product_id, seller_id, quantity=1):
        existing_item = CartItem.find_cart_item(cart_id, product_id)
        if existing_item:
            # Update quantity if item already exists
            new_quantity = existing_item.quantity + quantity
            app.db.execute('''
                UPDATE Cart_items
                SET quantity = :quantity, added_at = CURRENT_TIMESTAMP
                WHERE cart_item_id = :cart_item_id
            ''', quantity=new_quantity, cart_item_id=existing_item.cart_item_id)
            return existing_item
        else:
            # Insert new cart item
            rows = app.db.execute('''
                INSERT INTO Cart_items (cart_id, product_id, seller_id, quantity)
                VALUES (:cart_id, :product_id, :seller_id, :quantity)
                RETURNING cart_item_id, cart_id, product_id, seller_id, quantity, added_at
            ''', cart_id=cart_id, product_id=product_id, seller_id=seller_id, quantity=quantity)
            return CartItem(*rows[0]) if rows else None


    @staticmethod
    def find_cart_item(cart_id, product_id):
        rows = app.db.execute('''
            SELECT cart_item_id, cart_id, product_id, seller_id, quantity, added_at
            FROM Cart_items
            WHERE cart_id = :cart_id AND product_id = :product_id
        ''', cart_id=cart_id, product_id=product_id)
        return CartItem(*rows[0]) if rows else None

    @staticmethod
    def remove_from_cart(cart_item_id):
        app.db.execute('''
DELETE FROM Cart_items
WHERE cart_item_id = :cart_item_id
''', cart_item_id=cart_item_id)
        return True

    @staticmethod
    def clear_cart(cart_id):
        app.db.execute('''
            DELETE FROM Cart_items
            WHERE cart_id = :cart_id
        ''', cart_id=cart_id)
        return True
