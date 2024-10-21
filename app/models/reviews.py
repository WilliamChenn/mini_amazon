from flask import current_app as app
from flask_login import current_user

class Reviews:
    def __init__(self, review_id, seller_id, reviewer_id, product_id, rating, comment, created_at, updated_at):
        self.review_id = review_id
        self.seller_id = seller_id
        self.reviewer_id = reviewer_id
        self.product_id = product_id
        self.rating = rating
        self.comment = comment
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def get_by_product(product_id):
        rows = app.db.execute('''
SELECT review_id, seller_id, reviewer_id, product_id, rating, comment, created_at, updated_at
FROM Reviews
WHERE product_id = :product_id
''', product_id=product_id)
        return [Reviews(*row) for row in rows]

    @staticmethod
    def get_by_seller(seller_id):
        rows = app.db.execute('''
SELECT review_id, seller_id, reviewer_id, product_id, rating, comment, created_at, updated_at
FROM Reviews
WHERE seller_id = :seller_id
''', seller_id=seller_id)
        return [Reviews(*row) for row in rows]
    
    @staticmethod
    def get_by_user_id(reviewer_id):
        rows = app.db.execute('''
SELECT review_id, seller_id, reviewer_id, product_id, rating, comment, created_at, updated_at
FROM Reviews
WHERE reviewer_id = :reviewer_id
''', reviewer_id=reviewer_id, current_user=current_user)
        return [Reviews(*row) for row in rows]
