from flask import current_app as app

class Cart:
    def __init__(self, cart_id, user_id, created_at):
        self.cart_id = cart_id
        self.user_id = user_id
        self.created_at = created_at

    @staticmethod
    def get_cart(user_id):
        rows = app.db.execute('''
SELECT cart_id, user_id, created_at
FROM Carts
WHERE user_id = :user_id
''', user_id=user_id)
        return Cart(*rows[0]) if rows else None

    @staticmethod
    def create_cart(user_id):
        rows = app.db.execute('''
INSERT INTO Carts (user_id)
VALUES (:user_id)
RETURNING cart_id, user_id, created_at
''', user_id=user_id)
        return Cart(*rows[0]) if rows else None