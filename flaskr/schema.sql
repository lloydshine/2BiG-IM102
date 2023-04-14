-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS deliveries;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  fullname TEXT NOT NULL,
  phone_number TEXT NOT NULL,
  address TEXT NOT NULL,
  image_filename TEXT,
  account_type TEXT NOT NULL CHECK (account_type IN ('customer', 'admin', 'delivery')),
  date_joined TIMESTAMP DEFAULT (datetime('now','localtime'))
);

CREATE TABLE products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name INTEGER NOT NULL,
  description TEXT NOT NULL,
  image_filename TEXT NOT NULL,
  price INTEGER NOT NULL
);


CREATE TABLE orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  customer_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  total_price INTEGER NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('pending', 'taken', 'cancelled')) DEFAULT 'pending',
  address TEXT NOT NULL,
  date_ordered TIMESTAMP DEFAULT (datetime('now','localtime')),
  FOREIGN KEY (customer_id) REFERENCES users (id),
  FOREIGN KEY (product_id) REFERENCES products (id)
);

CREATE TABLE deliveries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id INTEGER NOT NULL,
  worker_id INTEGER NOT NULL,
  date_taken TIMESTAMP DEFAULT (datetime('now','localtime')),
  status TEXT NOT NULL CHECK (status IN ('pending', 'delivered', 'cancelled')) DEFAULT 'pending',
  date_delivered TIMESTAMP,
  FOREIGN KEY (order_id) REFERENCES orders (id),
  FOREIGN KEY (worker_id) REFERENCES users (id)
);

INSERT INTO users (username, password, fullname, phone_number, address, account_type)
VALUES
    ('admin', 'admin', 'Abdul Badar', '1234567890', 'Iligan City', 'admin'),
    ('lloyd', 'lloyd123', 'Lloyd Semblante', '1234567890', 'Iligan City', 'customer'),
    ('nurkeymar', 'nurkeymar123', 'Abdul Nurkeymar', '1234567890', 'Iligan City', 'delivery');

INSERT INTO products (name, description, image_filename, price)
VALUES
    ('Water Gallon', '10 Liters Gallon', '1.jpg', 50),
    ('Water Container', '12 Litters Gallon with faucet', '2.jpg', 120),
    ('Water Bottles', '8 Water Bottles', '3.jpg', 120),
    ('AquaFlask Bottle', 'Rich Kids Water Bottle', '5.png', 1200);
