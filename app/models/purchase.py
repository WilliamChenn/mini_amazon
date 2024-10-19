from flask import current_app as app


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
''',
                              purchase_id=purchase_id)
        return Purchase(*rows[0]) if rows else None

    @staticmethod
    def get_all_for_user(user_id):
        rows = app.db.execute('''
SELECT purchase_id, user_id, product_id, time_purchased
FROM Purchases
WHERE user_id = :user_id
''',
                              user_id=user_id)
        return [Purchase(*row) for row in rows]
