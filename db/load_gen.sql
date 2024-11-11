-- Load data into Users table
\COPY Users FROM '../generated/Users.csv' WITH DELIMITER ',' NULL '' CSV
-- Adjust auto-increment counter for Users table
SELECT pg_catalog.setval('users_user_id_seq',
                         (SELECT MAX(user_id)+1 FROM Users),
                         false);
-- Load data into Categories table before Products
\COPY Categories FROM '../generated/Categories.csv' WITH DELIMITER ',' NULL '' CSV
-- Adjust auto-increment counter for Categories table
SELECT pg_catalog.setval('categories_category_id_seq',
                         (SELECT MAX(category_id)+1 FROM Categories),
                         false);
-- Load data into Products table after Categories
\COPY Products FROM '../generated/Products.csv' WITH DELIMITER ',' NULL '' CSV
-- Adjust auto-increment counter for Products table
SELECT pg_catalog.setval('products_product_id_seq',
                         (SELECT MAX(product_id)+1 FROM Products),
                         false);
-- Load data into Seller_Products table
\COPY Seller_Products FROM '../generated/Seller_Products.csv' WITH DELIMITER ',' NULL '' CSV;
-- Load data into Product_Categories table
\COPY Product_Categories FROM '../generated/Product_Categories.csv' WITH DELIMITER ',' NULL '' CSV;
-- Load data into Carts table after Users
\COPY Carts FROM '../generated/Carts.csv' WITH DELIMITER ',' NULL '' CSV
-- Adjust auto-increment counter for Carts table
SELECT pg_catalog.setval('carts_cart_id_seq',
                         (SELECT MAX(cart_id)+1 FROM Carts),
                         false);
-- Load data into Cart_items table after Products and Carts
\COPY Cart_items FROM '../generated/Cart_items.csv' WITH DELIMITER ',' NULL '' CSV
-- Adjust auto-increment counter for Cart_items table
SELECT pg_catalog.setval('cart_items_cart_item_id_seq',
                         (SELECT MAX(cart_item_id)+1 FROM Cart_items),
                         false);
-- Load data into Orders table
\COPY Orders FROM '../generated/Orders.csv' WITH DELIMITER ',' NULL '' CSV
-- Adjust auto-increment counter for Orders table
SELECT pg_catalog.setval('orders_order_id_seq',
                         (SELECT MAX(order_id)+1 FROM Orders),
                         false);
-- Load data into Order_Items table
\COPY Order_Items FROM '../generated/Order_Items.csv' WITH DELIMITER ',' NULL '' CSV
-- Adjust auto-increment counter for Order_Items table
SELECT pg_catalog.setval('order_items_order_item_id_seq',
                         (SELECT MAX(order_item_id)+1 FROM Order_Items),
                         false);
-- Load data into Inventory table
\COPY Inventory FROM '../generated/Inventory.csv' WITH DELIMITER ',' NULL '' CSV
-- Adjust auto-increment counter for Inventory table
SELECT pg_catalog.setval('inventory_inventory_id_seq',
                         (SELECT MAX(inventory_id)+1 FROM Inventory),
                         false);