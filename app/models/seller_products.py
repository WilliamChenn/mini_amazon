from flask import current_app as app

class SellerProduct:
    def __init__(self, seller_id, product_id):
        self.seller_id = seller_id
        self.product_id = product_id

    @staticmethod
    def get_products_for_seller(seller_id):
        """
        Retrieve all products associated with a specific seller.
        """
        rows = app.db.execute('''
            SELECT seller_id, product_id
            FROM Seller_Products
            WHERE seller_id = :seller_id
        ''', seller_id=seller_id)
        return [SellerProduct(*row) for row in rows] if rows else []

    @staticmethod
    def get_sellers_for_product(product_id):
        """
        Retrieve all sellers associated with a specific product.
        """
        rows = app.db.execute('''
            SELECT seller_id, product_id
            FROM Seller_Products
            WHERE product_id = :product_id
        ''', product_id=product_id)
        return [SellerProduct(*row) for row in rows] if rows else []

    @staticmethod
    def add_seller_product(seller_id, product_id):
        """
        Associate a seller with a product.
        """
        try:
            app.db.execute('''
                INSERT INTO Seller_Products (seller_id, product_id)
                VALUES (:seller_id, :product_id)
            ''', seller_id=seller_id, product_id=product_id)
            return True
        except Exception as e:
            app.logger.error(f"Error adding seller-product association: {e}")
            return False

    @staticmethod
    def remove_seller_product(seller_id, product_id):
        """
        Remove the association between a seller and a product.
        """
        try:
            app.db.execute('''
                DELETE FROM Seller_Products
                WHERE seller_id = :seller_id AND product_id = :product_id
            ''', seller_id=seller_id, product_id=product_id)
            return True
        except Exception as e:
            app.logger.error(f"Error removing seller-product association: {e}")
            return False

    @staticmethod
    def find_seller_product(seller_id, product_id):
        """
        Check if a seller-product association exists.
        """
        rows = app.db.execute('''
            SELECT seller_id, product_id
            FROM Seller_Products
            WHERE seller_id = :seller_id AND product_id = :product_id
        ''', seller_id=seller_id, product_id=product_id)
        return SellerProduct(*rows[0]) if rows else None
