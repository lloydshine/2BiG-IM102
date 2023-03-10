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
  phone_number TEXT NOT NULL,
  account_type TEXT NOT NULL CHECK (account_type IN ('customer', 'admin', 'delivery')),
  date_joined TIMESTAMP DEFAULT (datetime('now','localtime'))
);

CREATE TABLE products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name INTEGER NOT NULL,
  description TEXT NOT NULL,
  price INTEGER NOT NULL,
  stock INTEGER NOT NULL
);
CREATE TABLE orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  customer_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  date_ordered TIMESTAMP DEFAULT (datetime('now','localtime')),
  FOREIGN KEY (customer_id) REFERENCES users (id),
  FOREIGN KEY (product_id) REFERENCES products (id)
);

CREATE TABLE deliveries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id INTEGER NOT NULL,
  worker_id INTEGER NOT NULL,
  date_delivered TIMESTAMP DEFAULT (datetime('now','localtime')),
  FOREIGN KEY (order_id) REFERENCES orders (id),
  FOREIGN KEY (worker_id) REFERENCES users (id)
);
