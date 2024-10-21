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
    
    @staticmethod
    def create(order_id, product_id, seller_id, quantity, unit_price, total_price, fulfillment_status='Pending'):
        rows = app.db.execute('''
            INSERT INTO Order_Items (order_id, product_id, seller_id, quantity, unit_price, total_price, fulfillment_status)
            VALUES (:order_id, :product_id, :seller_id, :quantity, :unit_price, :total_price, :fulfillment_status)
            RETURNING order_item_id, order_id, product_id, seller_id, quantity, unit_price, total_price, fulfillment_status, fulfilled_at
        ''', order_id=order_id, product_id=product_id, seller_id=seller_id, quantity=quantity,
           unit_price=unit_price, total_price=total_price, fulfillment_status=fulfillment_status)
        return OrderItem(*rows[0]) if rows else None

    @staticmethod
    def update_status(order_item_id, new_status):
        app.db.execute('''
            UPDATE Order_Items
            SET fulfillment_status = :new_status,
                fulfilled_at = CASE WHEN :new_status = 'Fulfilled' THEN CURRENT_TIMESTAMP ELSE fulfilled_at END
            WHERE order_item_id = :order_item_id
        ''', new_status=new_status, order_item_id=order_item_id)
