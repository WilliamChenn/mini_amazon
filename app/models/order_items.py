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
        # Update the order item's status
        app.db.execute('''
            UPDATE Order_Items
            SET fulfillment_status = :new_status,
                fulfilled_at = CASE WHEN :new_status = 'Fulfilled' THEN CURRENT_TIMESTAMP ELSE fulfilled_at END
            WHERE order_item_id = :order_item_id
        ''', new_status=new_status, order_item_id=order_item_id)

        # Get the order_id for the updated order item
        order_id = app.db.execute('''
            SELECT order_id FROM Order_Items WHERE order_item_id = :order_item_id
        ''', order_item_id=order_item_id)[0][0]

        # Check if all order items in the order are fulfilled
        unfulfilled_items = app.db.execute('''
            SELECT COUNT(*) FROM Order_Items
            WHERE order_id = :order_id AND fulfillment_status != 'Fulfilled'
        ''', order_id=order_id)[0][0]

        # Update the order's fulfillment status if necessary
        if unfulfilled_items == 0:
            app.db.execute('''
                UPDATE Orders
                SET fulfillment_status = 'Fulfilled'
                WHERE order_id = :order_id
            ''', order_id=order_id)

    @staticmethod
    def get_unfulfilled_order_items_by_seller_and_product(seller_id, product_id):
        rows = app.db.execute('''
            SELECT order_item_id, order_id, product_id, seller_id, quantity, unit_price, total_price, fulfillment_status, fulfilled_at
            FROM Order_Items
            WHERE seller_id = :seller_id
            AND product_id = :product_id
            AND fulfillment_status != 'Fulfilled'
        ''', seller_id=seller_id, product_id=product_id)
        return [OrderItem(*row) for row in rows]
