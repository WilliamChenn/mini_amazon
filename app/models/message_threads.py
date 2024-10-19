from flask import current_app as app

class MessageThread:
    def __init__(self, thread_id, order_id, created_at):
        self.thread_id = thread_id
        self.order_id = order_id
        self.created_at = created_at

    @staticmethod
    def get_by_order(order_id):
        rows = app.db.execute('''
SELECT thread_id, order_id, created_at
FROM Message_Threads
WHERE order_id = :order_id
''', order_id=order_id)
        return MessageThread(*rows[0]) if rows else None

    @staticmethod
    def create(order_id):
        rows = app.db.execute('''
INSERT INTO Message_Threads(order_id)
VALUES (:order_id)
RETURNING thread_id, order_id, created_at
''', order_id=order_id)
        return MessageThread(*rows[0])
