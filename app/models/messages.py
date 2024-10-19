from flask import current_app as app

class Message:
    def __init__(self, message_id, thread_id, sender_id, receiver_id, content, sent_at):
        self.message_id = message_id
        self.thread_id = thread_id
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content
        self.sent_at = sent_at

    @staticmethod
    def get_by_thread(thread_id):
        rows = app.db.execute('''
SELECT message_id, thread_id, sender_id, receiver_id, content, sent_at
FROM Messages
WHERE thread_id = :thread_id
''', thread_id=thread_id)
        return [Message(*row) for row in rows]

    @staticmethod
    def send_message(thread_id, sender_id, receiver_id, content):
        rows = app.db.execute('''
INSERT INTO Messages(thread_id, sender_id, receiver_id, content)
VALUES (:thread_id, :sender_id, :receiver_id, :content)
RETURNING message_id, thread_id, sender_id, receiver_id, content, sent_at
''', thread_id=thread_id, sender_id=sender_id, receiver_id=receiver_id, content=content)
        return Message(*rows[0])
