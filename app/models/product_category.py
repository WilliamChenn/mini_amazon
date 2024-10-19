from flask import current_app as app

class ProductCategory:
    def __init__(self, product_id, category_id):
        self.product_id = product_id
        self.category_id = category_id

    @staticmethod
    def get_categories_for_product(product_id):
        """
        Retrieve all categories for a specific product.
        """
        rows = app.db.execute("""
            SELECT c.category_id, c.category_name, c.parent_id
            FROM Categories c
            JOIN Product_Categories pc ON c.category_id = pc.category_id
            WHERE pc.product_id = :product_id
        """, product_id=product_id)
        return [Category(*row) for row in rows]

    @staticmethod
    def get_products_for_category(category_id):
        """
        Retrieve all products for a specific category.
        """
        rows = app.db.execute("""
            SELECT p.product_id, p.seller_id, p.name, p.summary, p.image_url, p.price, p.created_at, p.updated_at, p.available
            FROM Products p
            JOIN Product_Categories pc ON p.product_id = pc.product_id
            WHERE pc.category_id = :category_id
        """, category_id=category_id)
        return [Product(*row) for row in rows]

    @staticmethod
    def add_product_to_category(product_id, category_id):
        """
        Add a product to a category.
        """
        try:
            app.db.execute("""
                INSERT INTO Product_Categories(product_id, category_id)
                VALUES (:product_id, :category_id)
            """, product_id=product_id, category_id=category_id)
            return True
        except Exception as e:
            print(f"Error adding product to category: {e}")
            return False

    @staticmethod
    def remove_product_from_category(product_id, category_id):
        """
        Remove a product from a category.
        """
        try:
            app.db.execute("""
                DELETE FROM Product_Categories
                WHERE product_id = :product_id AND category_id = :category_id
            """, product_id=product_id, category_id=category_id)
            return True
        except Exception as e:
            print(f"Error removing product from category: {e}")
            return False
