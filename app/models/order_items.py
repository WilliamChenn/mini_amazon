from flask import current_app as app

class OrderItem:
    def __init__(self, order_item_id, order_id, product_id, seller_id, quantity, unit_price, total_price, fulfillment_status, fulfilled_at):
        self.order_item_id = order_item_id
        self.order_id = order_id
        self.product_id = product_id
        self.seller_id = seller_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_price = total_price
        self.fulfillment_status = fulfillment_status
        self.fulfilled_at = fulfilled_at

    @staticmethod
    def get(order_item_id):
        rows = app.db.execute('''
SELECT order_item_id, order_id, product_id, seller_id, quantity, unit_price, total_price, fulfillment_status, fulfilled_at
FROM Order_Items
WHERE order_item_id = :order_item_id
''', order_item_id=order_item_id)
        return OrderItem(*rows[0]) if rows else None

    @staticmethod
    def get_by_order(order_id):
        rows = app.db.execute('''
SELECT order_item_id, order_id, product_id, seller_id, quantity, unit_price, total_price, fulfillment_status, fulfilled_at
FROM Order_Items
WHERE order_id = :order_id
''', order_id=order_id)
        return [OrderItem(*row) for row in rows]
