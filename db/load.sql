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
