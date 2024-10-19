from flask import current_app as app
from datetime import datetime

class Purchase:
    def __init__(self, purchase_id, user_id, product_id, time_purchased):
        self.purchase_id = purchase_id
        self.user_id = user_id
        self.product_id = product_id
        self.time_purchased = time_purchased

    @staticmethod
    def get(purchase_id):
        rows = app.db.execute('''
            SELECT purchase_id, user_id, product_id, time_purchased
            FROM Purchases
            WHERE purchase_id = :purchase_id
        ''', purchase_id=purchase_id)
        return Purchase(*rows[0]) if rows else None

    @staticmethod
    def get_all_for_user(user_id):
        rows = app.db.execute('''
            SELECT purchase_id, user_id, product_id, time_purchased
            FROM Purchases
            WHERE user_id = :user_id
        ''', user_id=user_id)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_all_by_uid_since(uid, since):
        """
        Retrieves all purchases made by a user with user_id=uid since the specified datetime.

        Parameters:
            uid (int): The user ID.
            since (str or datetime): The datetime from which to retrieve purchases. 
                                      Can be a string in 'YYYY-MM-DD HH:MM:SS' format or a datetime object.

        Returns:
            List[Purchase]: A list of Purchase objects matching the criteria.
        """
        # Ensure 'since' is a string in the correct format
        if isinstance(since, datetime):
            since_str = since.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(since, str):
            # Optionally, validate the string format here
            since_str = since
        else:
            raise ValueError("Parameter 'since' must be a datetime object or a string in 'YYYY-MM-DD HH:MM:SS' format.")

        rows = app.db.execute('''
            SELECT purchase_id, user_id, product_id, time_purchased
            FROM Purchases
            WHERE user_id = :user_id AND time_purchased >= :since
            ORDER BY time_purchased DESC
        ''', user_id=uid, since=since_str)

        return [Purchase(*row) for row in rows]
