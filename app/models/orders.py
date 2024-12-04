from flask import current_app as app
from datetime import datetime

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
    def create(user_id, total_amount, num_items, fulfillment_status='Pending'):
        created_at = updated_at = datetime.utcnow()
        rows = app.db.execute('''
            INSERT INTO Orders (user_id, total_amount, num_items, fulfillment_status, created_at, updated_at)
            VALUES (:user_id, :total_amount, :num_items, :fulfillment_status, :created_at, :updated_at)
            RETURNING order_id, user_id, total_amount, num_items, fulfillment_status, created_at, updated_at
        ''', user_id=user_id, total_amount=total_amount, num_items=num_items,
           fulfillment_status=fulfillment_status, created_at=created_at, updated_at=updated_at)
        return Order(*rows[0]) if rows else None
    
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
    @staticmethod
    def update_status(order_id, new_status):
        updated_at = datetime.utcnow()
        app.db.execute('''
            UPDATE Orders
            SET fulfillment_status = :new_status,
                updated_at = :updated_at
            WHERE order_id = :order_id
        ''', new_status=new_status, updated_at=updated_at, order_id=order_id)
        
    @staticmethod
    def get_order_by_user_id(user_id, product_id):
        rows = app.db.execute('''
            SELECT o.order_id
            FROM Orders o
            JOIN Order_Items i ON o.order_id = i.order_id
            WHERE o.user_id = :user_id
            AND i.product_id = :product_id
        ''', user_id=user_id, product_id=product_id)
        # Return the fetched order_id(s)
        return len(rows) > 0
    
    @staticmethod
    def get_order_by_user_id_seller(user_id, seller_id):
        rows = app.db.execute('''
            SELECT o.order_id
            FROM Orders o
            JOIN Order_Items i ON o.order_id = i.order_id
            WHERE o.user_id = :user_id
            AND i.seller_id = :seller_id
        ''', user_id=user_id, seller_id=seller_id)
        # Return the fetched order_id(s)
        return len(rows) > 0

    
    @staticmethod
    def get_all_by_uid_since(user_id, since, limit=None):
        # Ensure 'since' is a string in the correct format
        if isinstance(since, datetime):
            since_str = since.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(since, str):
            # Optionally, validate the string format here
            since_str = since
        else:
            raise ValueError("Parameter 'since' must be a datetime object or a string in 'YYYY-MM-DD HH:MM:SS' format.")

        query = '''
            SELECT order_id, user_id, total_amount, num_items, fulfillment_status, created_at, updated_at
            FROM Orders
            WHERE user_id = :user_id AND created_at >= :since
            ORDER BY created_at DESC
        '''
        params = {'user_id': user_id, 'since': since_str}
        
        if limit:
            query += ' LIMIT :limit'
            params['limit'] = limit
        
        rows = app.db.execute(query, **params)

        return [Order(*row) for row in rows]
