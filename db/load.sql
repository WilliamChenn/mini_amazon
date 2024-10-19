-- Load data into Users table
\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
-- Adjust auto-increment counter for Users table
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);

-- Load data into Categories table before Products
\COPY Categories FROM 'Categories.csv' WITH DELIMITER ',' NULL '' CSV
-- Adjust auto-increment counter for Categories table
SELECT pg_catalog.setval('public.categories_id_seq',
                         (SELECT MAX(id)+1 FROM Categories),
                         false);

-- Load data into Products table after Categories
\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
-- Adjust auto-increment counter for Products table
SELECT pg_catalog.setval('public.products_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false);

-- Load data into Purchases table after Users and Products
\COPY Purchases FROM 'Purchases.csv' WITH DELIMITER ',' NULL '' CSV
-- Adjust auto-increment counter for Purchases table
SELECT pg_catalog.setval('public.purchases_id_seq',
                         (SELECT MAX(id)+1 FROM Purchases),
                         false);
