from flask_login import UserMixin
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
""",
                                  email=email,
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
            return User.get(user_id)
        except Exception as e:
            # Enhanced error handling
            print(f"Error registering user: {str(e)}")
            return None

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