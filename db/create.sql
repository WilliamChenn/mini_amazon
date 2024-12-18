-- Create Users table with updated schema
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    address TEXT,
    password VARCHAR(255) NOT NULL,
    balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    account_number VARCHAR(36) UNIQUE NOT NULL,
    public_name VARCHAR(255) NOT NULL,
    is_seller BOOLEAN NOT NULL DEFAULT FALSE,
    summary TEXT
);

-- Create Categories table with hierarchical structure
CREATE TABLE Categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(255) UNIQUE NOT NULL,
    parent_id INT REFERENCES Categories(category_id) ON DELETE
    SET
        NULL -- Hierarchical structure
);

-- Create Products table, as it depends on Categories and Users
CREATE TABLE Products (
    product_id SERIAL PRIMARY KEY,
    seller_id INT NOT NULL REFERENCES Users(user_id),
    -- References Users table
    category_id INT REFERENCES Categories(category_id),
    -- References Categories table
    name VARCHAR(255) UNIQUE NOT NULL,
    summary TEXT NOT NULL,
    image_url TEXT NOT NULL,
    price DECIMAL(12, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    available BOOLEAN DEFAULT TRUE -- Add available column
);

-- Create Seller_Products table to support many-to-many relationship between sellers and products
CREATE TABLE Seller_Products (
    seller_id INT NOT NULL REFERENCES Users(user_id),
    -- References Users table for sellers
    product_id INT NOT NULL REFERENCES Products(product_id),
    -- References Products table
    PRIMARY KEY (seller_id, product_id)
);

-- Create Product_Categories table (many-to-many relationship)
CREATE TABLE Product_Categories (
    product_id INT NOT NULL REFERENCES Products(product_id),
    category_id INT NOT NULL REFERENCES Categories(category_id),
    PRIMARY KEY (product_id, category_id)
);

-- Create Carts table for persistent user carts
CREATE TABLE Carts (
    cart_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL UNIQUE REFERENCES Users(user_id),
    -- Each user has one unique cart
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL -- Automatically set to current time
);

-- Create Cart_items table linking products and carts
CREATE TABLE Cart_items (
    cart_item_id SERIAL PRIMARY KEY,
    cart_id INT NOT NULL REFERENCES Carts(cart_id),
    -- References Carts table
    product_id INT NOT NULL REFERENCES Products(product_id),
    -- References Products table
    seller_id INT NOT NULL REFERENCES Users(user_id),
    -- References Users table for the seller
    quantity INT CHECK (quantity > 0) NOT NULL,
    -- Quantity must be greater than 0
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL -- Automatically set to current time
);

-- Create Orders table
CREATE TABLE Orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES Users(user_id),
    -- References Users table
    total_amount DECIMAL(10, 2) NOT NULL,
    num_items INT NOT NULL,
    fulfillment_status VARCHAR(50) NOT NULL CHECK (
        fulfillment_status IN ('Pending', 'Shipped', 'Fulfilled')
    ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create Order_Items table
CREATE TABLE Order_Items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL REFERENCES Orders(order_id),
    -- References Orders table
    product_id INT NOT NULL REFERENCES Products(product_id),
    -- References Products table
    seller_id INT NOT NULL REFERENCES Users(user_id),
    -- References Users table
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    fulfillment_status VARCHAR(50) NOT NULL CHECK (
        fulfillment_status IN ('Pending', 'Shipped', 'Fulfilled')
    ),
    fulfilled_at TIMESTAMP
);

-- Create Inventory table
CREATE TABLE Inventory (
    inventory_id SERIAL PRIMARY KEY,
    seller_id INT NOT NULL REFERENCES Users(user_id),
    -- References Users table
    product_id INT NOT NULL REFERENCES Products(product_id),
    -- References Products table
    quantity INT NOT NULL CHECK (quantity >= 0),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create Transactions table
CREATE TABLE Transactions (
    transaction_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES Users(user_id),
    -- References Users table
    transaction_type VARCHAR(50) NOT NULL CHECK (transaction_type IN ('Deposit', 'Withdrawal')),
    amount DECIMAL(10, 2) NOT NULL CHECK (amount > 0),
    balance_after DECIMAL(10, 2) NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create Reviews table
CREATE TABLE Reviews (
    review_id SERIAL PRIMARY KEY,
    seller_id INT REFERENCES Users(user_id),
    -- References Users table (for sellers)
    reviewer_id INT NOT NULL REFERENCES Users(user_id),
    -- References Users table (for reviewers)
    product_id INT REFERENCES Products(product_id),
    -- References Products table
    rating INT NOT NULL CHECK (
        rating BETWEEN 1
        AND 5
    ),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    product_seller BOOLEAN NOT NULL
);

-- Create Review_Images table
CREATE TABLE Review_Images (
    image_id SERIAL PRIMARY KEY,
    review_id INT NOT NULL REFERENCES Reviews(review_id),
    -- References Reviews table
    image_url TEXT NOT NULL
);

-- Create Message_Threads table
CREATE TABLE Message_Threads (
    thread_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL REFERENCES Orders(order_id),
    -- References Orders table
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create Messages table
CREATE TABLE Messages (
    message_id SERIAL PRIMARY KEY,
    thread_id INT NOT NULL REFERENCES Message_Threads(thread_id),
    -- References Message_Threads table
    sender_id INT NOT NULL REFERENCES Users(user_id),
    -- References Users table (sender)
    receiver_id INT NOT NULL REFERENCES Users(user_id),
    -- References Users table (receiver)
    content TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);