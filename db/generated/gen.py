import csv
from faker import Faker
from werkzeug.security import generate_password_hash
import random
import os

fake = Faker()
Faker.seed(0)
random.seed(0)

def get_csv_writer(f):
    return csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def gen_users(num_users):
    seller_ids = []
    ensure_directory('db/generated')
    with open('db/generated/Users.csv', 'w', newline='') as f:
        writer = get_csv_writer(f)
        print('Generating Users...', end=' ', flush=True)
        for uid in range(1, num_users + 1):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            email = fake.unique.email()
            first_name = fake.first_name()
            last_name = fake.last_name()
            address = fake.address().replace('\n', ', ')
            password = generate_password_hash(f'pass{uid}')
            balance = round(random.uniform(0, 1000), 2)
            account_number = fake.unique.bban()
            public_name = f"{first_name} {last_name}"
            is_seller = random.choice(['TRUE', 'FALSE'])
            summary = fake.text(max_nb_chars=200)
            writer.writerow([
                uid, email, first_name, last_name,
                address, password, balance,
                account_number, public_name,
                is_seller, summary
            ])
            if is_seller == 'TRUE':
                seller_ids.append(uid)
        print(f'\n{num_users} Users generated.')
    return seller_ids

def gen_categories(num_categories, max_depth=3):
    with open('db/generated/Categories.csv', 'w', newline='') as f:
        writer = get_csv_writer(f)
        print('Generating Categories...', end=' ', flush=True)
        category_id = 0  # Starting from 0 to align with your working example
        categories = []
        initial_categories = int(num_categories * 0.3)
        for _ in range(initial_categories):
            name = fake.unique.word().capitalize()
            writer.writerow([category_id, name, ''])  # parent_id is null
            categories.append({'id': category_id, 'name': name, 'parent_id': None, 'depth': 1})
            category_id += 1
        while category_id < num_categories:
            parent = random.choice(categories)
            if parent['depth'] >= max_depth:
                continue
            name = fake.unique.word().capitalize()
            writer.writerow([category_id, name, parent['id']])
            categories.append({
                'id': category_id,
                'name': name,
                'parent_id': parent['id'],
                'depth': parent['depth'] + 1
            })
            category_id += 1
        print(f'\n{num_categories} Categories generated.')

def gen_product_categories(num_product_categories, num_products, num_categories):
    with open('db/generated/Product_Categories.csv', 'w', newline='') as f:
        writer = get_csv_writer(f)
        print('Generating Product_Categories...', end=' ', flush=True)
        existing_pairs = set()
        for _ in range(num_product_categories):
            while True:
                product_id = random.randint(1, num_products)
                category_id = random.randint(0, num_categories - 1)  # Adjusted to match category_ids
                if (product_id, category_id) not in existing_pairs:
                    existing_pairs.add((product_id, category_id))
                    writer.writerow([product_id, category_id])
                    break
                if _ % 1000 == 0:
                    print(f'{_}', end=' ', flush=True)
        print(f'\n{num_product_categories} Product_Categories generated.')

def gen_seller_products(num_seller_products, product_sellers, seller_ids, num_products):
    existing = set(product_sellers)
    with open('db/generated/Seller_Products.csv', 'w', newline='') as f:
        writer = get_csv_writer(f)
        print('Generating Seller_Products...', end=' ', flush=True)
        # Write existing product_seller pairs
        for seller_id, product_id in product_sellers:
            writer.writerow([seller_id, product_id])
        # Now generate additional seller-product pairs
        while len(existing) < num_seller_products:
            seller_id = random.choice(seller_ids)
            product_id = random.randint(1, num_products)
            if (seller_id, product_id) not in existing:
                existing.add((seller_id, product_id))
                writer.writerow([seller_id, product_id])
        print(f'\n{len(existing)} Seller_Products generated.')
    return list(existing)

def gen_products(num_products, seller_ids, num_categories):
    product_sellers = []
    with open('db/generated/Products.csv', 'w', newline='') as f:
        writer = get_csv_writer(f)
        print('Generating Products...', end=' ', flush=True)
        for pid in range(1, num_products + 1):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            seller_id = random.choice(seller_ids)
            category_id = random.randint(0, num_categories - 1)  # Adjusted to match category_ids
            name = fake.unique.word().capitalize()
            summary = fake.text(max_nb_chars=200)
            image_url = fake.image_url()
            price = round(random.uniform(5, 500), 2)
            created_at_dt = fake.date_time_between(start_date='-1y', end_date='now')
            updated_at_dt = fake.date_time_between(start_date=created_at_dt, end_date='now')
            created_at = created_at_dt.strftime('%Y-%m-%d %H:%M:%S')
            updated_at = updated_at_dt.strftime('%Y-%m-%d %H:%M:%S')
            available = 'TRUE'
            writer.writerow([
                pid, seller_id, category_id, name,
                summary, image_url, price,
                created_at, updated_at, available
            ])
            product_sellers.append((seller_id, pid))
        print(f'\n{num_products} Products generated.')
    return product_sellers

def gen_inventory(num_inventory, seller_product_pairs):
    with open('db/generated/Inventory.csv', 'w', newline='') as f:
        writer = get_csv_writer(f)
        print('Generating Inventory...', end=' ', flush=True)
        for iid in range(1, num_inventory + 1):
            seller_id, product_id = random.choice(seller_product_pairs)
            quantity = random.randint(0, 100)
            updated_at = fake.date_time_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([iid, seller_id, product_id, quantity, updated_at])
            if iid % 1000 == 0:
                print(f'{iid}', end=' ', flush=True)
        print(f'\n{num_inventory} Inventory records generated.')

def gen_carts(num_users):
    with open('db/generated/Carts.csv', 'w', newline='') as f:
        writer = get_csv_writer(f)
        print('Generating Carts...', end=' ', flush=True)
        for cid in range(1, num_users + 1):
            user_id = cid
            created_at = fake.date_time_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([cid, user_id, created_at])
        print(f'\nCarts generated.')

def gen_cart_items(num_cart_items, num_carts, seller_product_pairs):
    with open('db/generated/Cart_items.csv', 'w', newline='') as f:
        writer = get_csv_writer(f)
        print('Generating Cart_Items...', end=' ', flush=True)
        for ciid in range(1, num_cart_items + 1):
            cart_id = random.randint(1, num_carts)
            seller_id, product_id = random.choice(seller_product_pairs)
            quantity = random.randint(1, 5)
            added_at = fake.date_time_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([ciid, cart_id, product_id, seller_id, quantity, added_at])
            if ciid % 1000 == 0:
                print(f'{ciid}', end=' ', flush=True)
        print(f'\n{num_cart_items} Cart_Items generated.')

def gen_orders(num_orders, num_users):
    with open('db/generated/Orders.csv', 'w', newline='') as f:
        writer = get_csv_writer(f)
        print('Generating Orders...', end=' ', flush=True)
        for oid in range(1, num_orders + 1):
            if oid % 100 == 0:
                print(f'{oid}', end=' ', flush=True)
            user_id = random.randint(1, num_users)
            total_amount = round(random.uniform(20, 1000), 2)
            num_items = random.randint(1, 10)
            fulfillment_status = random.choice(['Pending', 'Shipped', 'Fulfilled'])
            created_at_dt = fake.date_time_between(start_date='-1y', end_date='now')
            updated_at_dt = fake.date_time_between(start_date=created_at_dt, end_date='now')
            created_at_str = created_at_dt.strftime('%Y-%m-%d %H:%M:%S')
            updated_at_str = updated_at_dt.strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([
                oid, user_id, total_amount, num_items,
                fulfillment_status, created_at_str, updated_at_str
            ])
        print(f'\n{num_orders} Orders generated.')

def gen_order_items(num_order_items, num_orders, seller_product_pairs):
    with open('db/generated/Order_Items.csv', 'w', newline='') as f:
        writer = get_csv_writer(f)
        print('Generating Order_Items...', end=' ', flush=True)
        for oiid in range(1, num_order_items + 1):
            order_id = random.randint(1, num_orders)
            seller_id, product_id = random.choice(seller_product_pairs)
            quantity = random.randint(1, 5)
            unit_price = round(random.uniform(5, 500), 2)
            total_price = round(unit_price * quantity, 2)
            fulfillment_status = random.choice(['Pending', 'Shipped', 'Fulfilled'])
            if fulfillment_status == 'Fulfilled':
                fulfilled_at_dt = fake.date_time_between(start_date='-1y', end_date='now')
                fulfilled_at = fulfilled_at_dt.strftime('%Y-%m-%d %H:%M:%S')
            else:
                fulfilled_at = ''  # Null value represented as empty field
            writer.writerow([
                oiid, order_id, product_id, seller_id,
                quantity, unit_price, total_price,
                fulfillment_status, fulfilled_at
            ])
            if oiid % 1000 == 0:
                print(f'{oiid}', end=' ', flush=True)
        print(f'\n{num_order_items} Order_Items generated.')

def gen_reviews(num_reviews, num_users, seller_product_pairs):
    product_seller_map = {}
    for seller_id, product_id in seller_product_pairs:
        if product_id not in product_seller_map:
            product_seller_map[product_id] = []
        product_seller_map[product_id].append(seller_id)
    with open('db/generated/Reviews.csv', 'w', newline='') as f:
        writer = get_csv_writer(f)
        print('Generating Reviews...', end=' ', flush=True)
        for rid in range(1, num_reviews + 1):
            if rid % 100 == 0:
                print(f'{rid}', end=' ', flush=True)
            product_id = random.choice(list(product_seller_map.keys()))
            seller_id = random.choice(product_seller_map[product_id])
            reviewer_id = random.randint(1, num_users)
            # Ensure reviewer_id is not the seller_id
            while reviewer_id == seller_id:
                reviewer_id = random.randint(1, num_users)
            rating = random.randint(1, 5)
            comment = fake.text(max_nb_chars=200)
            created_at_dt = fake.date_time_between(start_date='-1y', end_date='now')
            updated_at_dt = fake.date_time_between(start_date=created_at_dt, end_date='now')
            created_at_str = created_at_dt.strftime('%Y-%m-%d %H:%M:%S')
            updated_at_str = updated_at_dt.strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([
                rid, seller_id, reviewer_id, product_id,
                rating, comment, created_at_str, updated_at_str
            ])
        print(f'\n{num_reviews} Reviews generated.')

def main():
    num_users = 100
    num_categories = 50
    num_products = 200
    num_product_categories = 300
    num_seller_products = 500
    num_cart_items = 500
    num_orders = 150
    num_order_items = 300
    num_inventory = 500
    num_reviews = 100

    seller_ids = gen_users(num_users)
    gen_categories(num_categories)
    product_sellers = gen_products(num_products, seller_ids, num_categories)
    seller_product_pairs = gen_seller_products(num_seller_products, product_sellers, seller_ids, num_products)
    gen_inventory(num_inventory, seller_product_pairs)
    gen_carts(num_users)
    gen_cart_items(num_cart_items, num_users, seller_product_pairs)
    gen_orders(num_orders, num_users)
    gen_order_items(num_order_items, num_orders, seller_product_pairs)
    gen_reviews(num_reviews, num_users, seller_product_pairs)
    gen_product_categories(num_product_categories, num_products, num_categories)

if __name__ == '__main__':
    main()
