from flask import current_app as app


class Category:
    def __init__(self, id, category_name, parent_id):
        self.id = id
        self.category_name = category_name
        self.parent_id = parent_id

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, category_name, parent_id
FROM Categories
WHERE id = :id
''', id=id)
        return Category(*rows[0]) if rows else None

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT id, category_name, parent_id
FROM Categories
''')
        return [Category(*row) for row in rows]

    @staticmethod
    def add(category_name, parent_id=None):
        try:
            rows = app.db.execute('''
INSERT INTO Categories(category_name, parent_id)
VALUES (:category_name, :parent_id)
RETURNING id
''', category_name=category_name, parent_id=parent_id)
            return rows[0][0]  # Return the newly created category ID
        except Exception as e:
            print(f"Error adding category: {str(e)}")
            return None

    @staticmethod
    def update(id, category_name=None, parent_id=None):
        try:
            app.db.execute('''
UPDATE Categories
SET category_name = COALESCE(:category_name, category_name),
    parent_id = COALESCE(:parent_id, parent_id)
WHERE id = :id
''', id=id, category_name=category_name, parent_id=parent_id)
            return True
        except Exception as e:
            print(f"Error updating category: {str(e)}")
            return False

    @staticmethod
    def delete(id):
        try:
            app.db.execute('''
DELETE FROM Categories
WHERE id = :id
''', id=id)
            return True
        except Exception as e:
            print(f"Error deleting category: {str(e)}")
            return False
