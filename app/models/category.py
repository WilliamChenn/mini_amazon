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
