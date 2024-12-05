from flask import current_app as app


class Category:
    def __init__(self, category_id, category_name, parent_id=None):
        self.category_id = category_id
        self.category_name = category_name
        self.parent_id = parent_id

    @staticmethod
    def get(category_id):
        rows = app.db.execute('''
            SELECT category_id, category_name, parent_id
            FROM Categories
            WHERE category_id = :category_id
        ''',
                              category_id=category_id)
        return Category(*rows[0]) if rows else None

    @staticmethod
    def get_all():
        rows = app.db.execute('''
            SELECT category_id, category_name, parent_id
            FROM Categories
        ''')
        return [Category(*row) for row in rows]

    @staticmethod
    def create(category_name, parent_id=None):
        try:
            rows = app.db.execute('''
                INSERT INTO Categories (category_name, parent_id)
                VALUES (:category_name, :parent_id)
                RETURNING category_id, category_name, parent_id
            ''',
                                  category_name=category_name,
                                  parent_id=parent_id)
            return Category(*rows[0]) if rows else None
        except Exception as e:
            app.logger.error(f"Error creating category: {e}")
            return None

    @staticmethod
    def get_children(parent_id):
        rows = app.db.execute('''
            SELECT category_id, category_name, parent_id
            FROM Categories
            WHERE parent_id = :parent_id
        ''', parent_id=parent_id)
        return [Category(*row) for row in rows]

    @staticmethod
    def get_all_subcategory_ids(category_id):
        # Fetch all categories
        categories = Category.get_all()
        categories_dict = {c.category_id: c for c in categories}
        subcategory_ids = []

        def recurse(current_id):
            subcategory_ids.append(current_id)
            for cat in categories:
                if cat.parent_id == current_id:
                    recurse(cat.category_id)

        recurse(category_id)
        return subcategory_ids

    @staticmethod
    def get_all_ancestor_ids(category_id):
        """Get all ancestor category IDs (parent, grandparent, etc)"""
        ancestors = []
        
        def recurse(current_id):
            row = app.db.execute('''
                SELECT parent_id 
                FROM Categories 
                WHERE category_id = :category_id 
                AND parent_id IS NOT NULL
            ''', category_id=current_id)
            if row and row[0][0]:
                parent_id = row[0][0]
                ancestors.append(parent_id)
                recurse(parent_id)
                
        recurse(category_id)
        return ancestors
