from flask import current_app as app




class Product:
   def __init__(self, id, name, price, available, seller_id, category_id, summary, created_at):
       self.id = id
       self.name = name
       self.price = price
       self.available = available
       self.seller_id = seller_id
       self.category_id = category_id
       self.summary = summary
       self.created_at = created_at


#implement method for removing a product
      
   @staticmethod
   def get(id):
       rows = app.db.execute('''
   SELECT id, name, price, available, seller_id, category_id, summary, created_at
   FROM Products
   WHERE id = :id
   ''',
                             id=id)
       return Product(*(rows[0])) if rows is not None else None


   @staticmethod
   def get_all(available=True):
       rows = app.db.execute('''
   SELECT id, name, price, available
   FROM Products
   WHERE available = :available
   ''',
                             available=available)
       return [Product(*row) for row in rows]
