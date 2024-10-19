from flask import current_app as app

class Order:
    def __init__(self, order_id, user_id, total_amount, num_items, fulfillment_status, created_at, updated_at):
        self.order_id = order_id
        self.user_id = user_id
        self.total_amount = total_amount
        self.num_items = num_items
        self.fulfillment_status = fulfillment_status
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def get(order_id):
        rows = app.db.execute('''
SELECT order_id, user_id, total_amount, num_items, fulfillment_status, created_at, updated_at
FROM Orders
WHERE order_id = :order_id
''', order_id=order_id)
        return Order(*rows[0]) if rows else None

    @staticmethod
    def get_by_user(user_id):
        rows = app.db.execute('''
SELECT order_id, user_id, total_amount, num_items, fulfillment_status, created_at, updated_at
FROM Orders
WHERE user_id = :user_id
''', user_id=user_id)
        return [Order(*row) for row in rows]
