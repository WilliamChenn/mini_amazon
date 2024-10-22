from flask_login import UserMixin
import os
import csv
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

from .. import login


class User(UserMixin):
    def __init__(self, user_id, email, first_name, last_name, address, password, balance, account_number, public_name, is_seller, summary):
        self.id = user_id  # Flask-Login expects `id` attribute
        self.user_id = user_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.password = password
        self.balance = balance
        self.account_number = account_number
        self.public_name = public_name
        self.is_seller = is_seller
        self.summary = summary

    @staticmethod
    def generate_account_number():
        # Generates a unique account number using UUID4
        return str(uuid.uuid4())

    @staticmethod
    def account_number_exists(account_number):
        rows = app.db.execute("""
SELECT account_number
FROM Users
WHERE account_number = :account_number
""",
                              account_number=account_number)
        return len(rows) > 0

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT user_id, email, first_name, last_name, address, password, balance, account_number, public_name, is_seller, summary
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        user_data = rows[0]
        stored_password = user_data[5]
        if not check_password_hash(stored_password, password):
            # incorrect password
            return None
        return User(*user_data)

    @staticmethod
    def register(email, password, first_name, last_name, address=None, summary=None):
        if User.email_exists(email):
            print("Email already in use.")
            return None
        try:
            account_number = User.generate_account_number()
            # Ensure account_number is unique
            while User.account_number_exists(account_number):
                account_number = User.generate_account_number()

            rows = app.db.execute("""
                INSERT INTO Users(email, password, first_name, last_name, address, balance, account_number, public_name, is_seller, summary)
                VALUES(:email, :password, :first_name, :last_name, :address, :balance, :account_number, :public_name, :is_seller, :summary)
                RETURNING user_id
            """, email=email,
               password=generate_password_hash(password),
               first_name=first_name,
               last_name=last_name,
               address=address,
               balance=0.00,  # Default value
               account_number=account_number,
               public_name=first_name,  # Or any other logic
               is_seller=False,  # Default value
               summary=summary)
            user_id = rows[0][0]
            user = User.get(user_id)

            # Write user data to CSV
            User.write_to_csv(user)

            return user
        except Exception as e:
            # Enhanced error handling
            print(f"Error registering user: {str(e)}")
            return None
        

    @staticmethod
    def write_to_csv(user):
        """
        Appends the user's data to the Users.csv file.

        Parameters:
            user (User): The user object to write to CSV.
        """
        try:
            # Determine the path to Users.csv relative to user.py
            # user.py is located at /home/ubuntu/shared/mini_amazon/app/models/user.py
            # Users.csv is at /home/ubuntu/shared/mini_amazon/db/data/Users.csv
            # Therefore, navigate up two directories and then to db/data/Users.csv
            base_dir = os.path.dirname(os.path.abspath(__file__))  # /home/ubuntu/shared/mini_amazon/app/models
            csv_path = os.path.join(base_dir, '../../db/data/Users.csv')
            csv_path = os.path.abspath(csv_path)  # Normalize the path

            # Open the CSV file in append mode
            with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)

                # Write the user data as a new row
                writer.writerow([
                    user.user_id,
                    user.email,
                    user.first_name,
                    user.last_name,
                    user.address if user.address else '',
                    user.password,
                    f"{user.balance:.2f}",  # Ensure two decimal places
                    user.account_number,
                    user.public_name,
                    user.is_seller,
                    user.summary if user.summary else ''
                ])
            print(f"User data written to CSV: {csv_path}")
        except Exception as e:
            print(f"Error writing user data to CSV: {str(e)}")

    @staticmethod
    @login.user_loader
    def get(user_id):
        rows = app.db.execute("""
SELECT user_id, email, first_name, last_name, address, password, balance, account_number, public_name, is_seller, summary
FROM Users
WHERE user_id = :user_id
""",
                              user_id=user_id)
        return User(*rows[0]) if rows else None


    @staticmethod
    def update_balance(user_id, new_balance):
        try:
            app.db.execute("""
    UPDATE Users
    SET balance = :new_balance
    WHERE user_id = :user_id
    """,
                        new_balance=new_balance,
                        user_id=user_id)
            return True
        except Exception as e:
            print(f"Error updating balance: {str(e)}")
            return False

    def update_address(self, new_address):
        try:
            app.db.execute("""
UPDATE Users
SET address = :new_address
WHERE user_id = :user_id
""",
                      new_address=new_address,
                      user_id=self.user_id)
            self.address = new_address
            return True
        except Exception as e:
            print(f"Error updating address: {str(e)}")
            return False

    def update_summary(self, new_summary):
        try:
            app.db.execute("""
UPDATE Users
SET summary = :new_summary
WHERE user_id = :user_id
""",
                      new_summary=new_summary,
                      user_id=self.user_id)
            self.summary = new_summary
            return True
        except Exception as e:
            print(f"Error updating summary: {str(e)}")
            return False