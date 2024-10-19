-- Load data into Users table
\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
-- Adjust auto-increment counter for Users table
SELECT pg_catalog.setval('users_user_id_seq',
                         (SELECT MAX(user_id)+1 FROM Users),
                         false);

-- Load data into Categories table before Products
\COPY Categories FROM 'Categories.csv' WITH DELIMITER ',' NULL '' CSV
-- Adjust auto-increment counter for Categories table
SELECT pg_catalog.setval('categories_category_id_seq',
                         (SELECT MAX(category_id)+1 FROM Categories),
                         false);

-- Load data into Products table after Categories
\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
-- Adjust auto-increment counter for Products table
SELECT pg_catalog.setval('products_product_id_seq',
                         (SELECT MAX(product_id)+1 FROM Products),
                         false);

-- Load data into Purchases table after Users and Products
\COPY Purchases FROM 'Purchases.csv' WITH DELIMITER ',' NULL '' CSV
-- Adjust auto-increment counter for Purchases table
SELECT pg_catalog.setval('purchases_purchase_id_seq',
                         (SELECT MAX(purchase_id)+1 FROM Purchases),
                         false);

-- Load data into Product_Categories table
\COPY Product_Categories FROM 'Product_Categories.csv' WITH DELIMITER ',' NULL '' CSV;

-- Load data into Carts table after Users
\COPY Carts FROM 'Carts.csv' WITH DELIMITER ',' NULL '' CSV
-- Adjust auto-increment counter for Carts table
SELECT pg_catalog.setval('carts_cart_id_seq',
                         (SELECT MAX(cart_id)+1 FROM Carts),
                         false);

-- Load data into Cart_items table after Products and Carts
\COPY Cart_items FROM 'Cart_items.csv' WITH DELIMITER ',' NULL '' CSV
-- Adjust auto-increment counter for Cart_items table
SELECT pg_catalog.setval('cart_items_cart_item_id_seq',
                         (SELECT MAX(cart_item_id)+1 FROM Cart_items),
                         false);

-- Load data into Orders table
\COPY Orders FROM 'Orders.csv' WITH DELIMITER ',' NULL '' CSV
-- Adjust auto-increment counter for Orders table
SELECT pg_catalog.setval('orders_order_id_seq',
                         (SELECT MAX(order_id)+1 FROM Orders),
                         false);

-- Load data into Order_Items table
\COPY Order_Items FROM 'Order_Items.csv' WITH DELIMITER ',' NULL '' CSV
-- Adjust auto-increment counter for Order_Items table
SELECT pg_catalog.setval('order_items_order_item_id_seq',
                         (SELECT MAX(order_item_id)+1 FROM Order_Items),
                         false);

-- Load data into Inventory table
\COPY Inventory FROM 'Inventory.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('inventory_inventory_id_seq', 
                        (SELECT MAX(inventory_id)+1 FROM Inventory), false);

-- Load data into Transactions table
\COPY Transactions FROM 'Transactions.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('transactions_transaction_id_seq', 
                        (SELECT MAX(transaction_id)+1 FROM Transactions), false);

-- Load data into Reviews table
\COPY Reviews FROM 'Reviews.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('reviews_review_id_seq', (SELECT MAX(review_id)+1 FROM Reviews), false);

-- Load data into Review_Images table
\COPY Review_Images FROM 'Review_Images.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('review_images_image_id_seq', 
                        (SELECT MAX(image_id)+1 FROM Review_Images), false);

-- Load data into Message_Threads table
\COPY Message_Threads FROM 'Message_Threads.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('message_threads_thread_id_seq', 
                        (SELECT MAX(thread_id)+1 FROM Message_Threads), false);

-- Load data into Messages table
\COPY Messages FROM 'Messages.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('messages_message_id_seq', 
                        (SELECT MAX(message_id)+1 FROM Messages), false);
