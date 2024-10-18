\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
-- pg_cataglog.setval allows for the next inserted entry value to be incremented by the last one appearing in the CSV
SELECT pg_catalog.setval('public.users_id_seq',
                        (SELECT MAX(id)+1 FROM Users),
                        false);


\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                        (SELECT MAX(id)+1 FROM Products),
                        false); 


-- add categories.csv, sellers.csv                               


\COPY Categories FROM 'Categories.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                        (SELECT MAX(id)+1 FROM Products),
                        false);                       


\COPY Purchases FROM 'Purchases.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.purchases_id_seq',
                        (SELECT MAX(id)+1 FROM Purchases),
                        false);
