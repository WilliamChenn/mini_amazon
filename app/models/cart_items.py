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
    def add_to_cart(cart_id, product_id, seller_id, quantity):
        rows = app.db.execute('''
INSERT INTO Cart_items (cart_id, product_id, seller_id, quantity)
VALUES (:cart_id, :product_id, :seller_id, :quantity)
RETURNING cart_item_id, cart_id, product_id, seller_id, quantity, added_at
''', cart_id=cart_id, product_id=product_id, seller_id=seller_id, quantity=quantity)
        return CartItem(*rows[0]) if rows else None

    @staticmethod
    def remove_from_cart(cart_item_id):
        app.db.execute('''
DELETE FROM Cart_items
WHERE cart_item_id = :cart_item_id
''', cart_item_id=cart_item_id)
        return True
