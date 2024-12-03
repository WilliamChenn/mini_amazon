from flask import current_app as app, render_template
from flask_login import current_user

class Reviews:
    def __init__(self, review_id, seller_id, reviewer_id, product_id, rating, comment, created_at, updated_at, product_name=None):
        self.review_id = review_id
        self.seller_id = seller_id
        self.reviewer_id = reviewer_id
        self.product_id = product_id
        self.rating = rating
        self.comment = comment
        self.created_at = created_at
        self.updated_at = updated_at
        self.product_name = product_name  # Optional: name of the product

    @staticmethod
    def get_by_id(review_id):
        rows = app.db.execute('''
            SELECT review_id, seller_id, reviewer_id, product_id, rating, comment, created_at, updated_at
            FROM Reviews
            WHERE review_id = :review_id
            ''', review_id=review_id)
        return Reviews(*(rows[0])) if rows else None

    @staticmethod
    def get_by_product(product_id):
        rows = app.db.execute('''
            SELECT review_id, seller_id, reviewer_id, product_id, rating, comment, created_at, updated_at
            FROM Reviews
            WHERE product_id = :product_id
            ORDER BY created_at DESC
        ''', product_id=product_id)
        return [Reviews(*row) for row in rows]

    @staticmethod
    def get_by_seller(seller_id):
        rows = app.db.execute('''
            SELECT r.review_id, r.seller_id, r.reviewer_id, r.product_id, r.rating, r.comment, r.created_at, r.updated_at
            FROM Reviews r
            JOIN Products p ON r.product_id = p.product_id
            WHERE p.seller_id = :seller_id
        ''', seller_id=seller_id)
        return [Reviews(*row) for row in rows]
    
    @staticmethod
    def get_reviews_by_user_id(reviewer_id):
        rows = app.db.execute('''
            SELECT
                r.review_id,
                r.seller_id,
                r.reviewer_id,
                r.product_id,
                r.rating,
                r.comment,
                r.created_at,
                r.updated_at,
                p.name AS product_name
            FROM Reviews r
            JOIN Products p ON r.product_id = p.product_id
            WHERE r.reviewer_id = :reviewer_id
            ORDER BY r.created_at DESC
        ''', reviewer_id=reviewer_id)

        return [Reviews(*row) for row in rows]
    
    @staticmethod
    def review_user_id_exists(user_id, product_id):
        rows = app.db.execute('''
            SELECT review_id
            FROM Reviews r
            WHERE r.reviewer_id = :reviewer_id
            AND r.product_id = :product_id
            ''', reviewer_id=user_id, product_id = product_id)
        return len(rows) > 0
    
    @staticmethod
    def update_review(review_id, rating, comment):
        app.db.execute('''
                UPDATE Reviews
                SET rating = :rating,
                    comment = :comment,
                    updated_at = NOW()
                WHERE review_id = :review_id
            ''',
            review_id=review_id,
            rating=rating,
            comment=comment)
        return True
    
    @staticmethod
    def create_review(seller_id, reviewer_id, product_id, rating, comment):
        app.db.execute('''
            INSERT INTO Reviews (seller_id, reviewer_id, product_id, rating, comment, created_at, updated_at)
            VALUES (:seller_id, :reviewer_id, :product_id, :rating, :comment, NOW(), NOW())
        ''',
        seller_id=seller_id,
        reviewer_id=reviewer_id,
        product_id=product_id,
        rating=rating,
        comment=comment)
        return True

    
    @staticmethod
    def delete_review(review_id):
        app.db.execute('''
                DELETE FROM Reviews
                WHERE review_id = :review_id
            ''',
            review_id=review_id)
        return True
    
    @staticmethod
    def get_seller_reviews():
        rows = app.db.execute('''
            SELECT u.user_id, u.first_name, AVG(r.rating) AS average_rating, MAX(r.created_at) AS latest_review_date, COUNT(r.rating) AS rating_count
            FROM Reviews r
            JOIN Users u ON r.seller_id = u.user_id
            GROUP BY r.seller_id, u.first_name, u.user_id
            ORDER BY average_rating DESC, latest_review_date DESC
        ''')
        return [
            {'id': row[0], 'name': row[1], 'average_rating': row[2], 'latest_review_date': row[3], 'review_count': row[4]}
            for row in rows
        ]

    @staticmethod
    def get_product_reviews():
        rows = app.db.execute('''
            SELECT p.product_id, p.name, AVG(r.rating) AS average_rating, MAX(r.created_at) AS latest_review_date, COUNT(r.rating) AS rating_count
            FROM Reviews r
            JOIN Products p ON r.product_id = p.product_id
            GROUP BY p.product_id, p.name
            ORDER BY average_rating DESC, latest_review_date DESC
        ''')
        return [
            {'id': row[0], 'name': row[1], 'average_rating': row[2], 'latest_review_date': row[3], 'review_count': row[4]}
            for row in rows
        ]



