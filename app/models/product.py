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
        return Product(*(rows[0])) if rows else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT product_id, seller_id, category_id, name, summary, image_url, price, created_at, updated_at, available
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_by_seller(seller_id):
        rows = app.db.execute('''
            SELECT p.product_id, p.seller_id, p.category_id, p.name, p.summary, p.image_url, p.price, p.created_at, p.updated_at, p.available
            FROM Products p
            JOIN seller_products sp ON p.product_id = sp.product_id
            WHERE sp.seller_id = :seller_id
        ''', seller_id=seller_id)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_by_category(category_id):
        rows = app.db.execute('''
SELECT product_id, seller_id, category_id, name, summary, image_url, price, created_at, updated_at, available
FROM Products
WHERE category_id = :category_id
''',
                              category_id=category_id)
        return [Product(*row) for row in rows]
    
    @staticmethod
    def create(seller_id, category_id, name, summary, image_url, price, available=True):
        try:
            rows = app.db.execute('''
                INSERT INTO Products (seller_id, category_id, name, summary, image_url, price, available)
                VALUES (:seller_id, :category_id, :name, :summary, :image_url, :price, :available)
                RETURNING product_id, seller_id, category_id, name, summary, image_url, price, created_at, updated_at, available
            ''', seller_id=seller_id, category_id=category_id, name=name, summary=summary, image_url=image_url, price=price, available=available)
            return Product(*rows[0]) if rows else None
        except Exception as e:
            app.logger.error(f"Error creating product: {e}")
            return None
