from flask import current_app as app

class Transaction:
    def __init__(self, transaction_id, user_id, transaction_type, amount, balance_after, transaction_date):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.balance_after = balance_after
        self.transaction_date = transaction_date

    @staticmethod
    def get_by_user(user_id):
        rows = app.db.execute('''
SELECT transaction_id, user_id, transaction_type, amount, balance_after, transaction_date
FROM Transactions
WHERE user_id = :user_id
''', user_id=user_id)
        return [Transaction(*row) for row in rows]
