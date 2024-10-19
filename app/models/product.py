from flask import current_app as app


class Product:
    def __init__(self, product_id, seller_id, category_id, name, summary, image_url, price, created_at, updated_at, available):
        self.product_id = product_id
        self.seller_id = seller_id
        self.category_id = category_id
        self.name = name
        self.summary = summary
        self.image_url = image_url
        self.price = price
        self.created_at = created_at
        self.updated_at = updated_at
        self.available = available

    @staticmethod
    def get(product_id):
        rows = app.db.execute('''
SELECT product_id, seller_id, category_id, name, summary, image_url, price, created_at, updated_at, available
FROM Products
WHERE product_id = :product_id
''',
                              product_id=product_id)
        return Product(*rows[0]) if rows else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT product_id, seller_id, category_id, name, summary, image_url, price, created_at, updated_at, available
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]
