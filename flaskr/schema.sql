-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS user_address;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS deliveries;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  fname TEXT NOT NULL,
  mname TEXT NOT NULL,
  lname TEXT NOT NULL,
  phone_number TEXT NOT NULL,
  image_filename TEXT,
  account_type TEXT NOT NULL CHECK (account_type IN ('customer', 'admin', 'delivery')),
  date_joined TIMESTAMP DEFAULT (datetime('now','localtime'))
);

CREATE TABLE user_address (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  street TEXT NOT NULL,
  city TEXT NOT NULL,
  house_no TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id)
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
  address INTEGER NOT NULL,
  date_ordered TIMESTAMP DEFAULT (datetime('now','localtime')),
  FOREIGN KEY (customer_id) REFERENCES users (id),
  FOREIGN KEY (product_id) REFERENCES products (id),
  FOREIGN KEY (address) REFERENCES user_address (id)
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

INSERT INTO users (username, password,fname,mname,lname, phone_number, account_type)
VALUES
    ('admin', 'admin', 'Abdul','Muhamad','Badar','1234567890','admin'),
    ('lloyd', 'lloyd123', 'Lloyd','Tutor','Semblante', '1234567890','customer'),
    ('nurkeymar', 'nurkeymar123', 'Abdul','Jabol','Nurkeymar', '1234567890','delivery');

INSERT INTO user_address (user_id, street, city, house_no)
VALUES
    (1, 'Barangay Maria Cristina', 'Iligan City', '002'),
    (2, 'Tubod Baruy', 'Iligan City', '078'),
    (3, 'Tibanga', 'Iligan City', '789');

INSERT INTO products (name, description, image_filename, price)
VALUES
    ('Water Gallon', '10 Liters Gallon', '1.jpg', 50),
    ('Water Container', '12 Litters Gallon with faucet', '2.jpg', 120),
    ('Water Bottles', '8 Water Bottles', '3.jpg', 120),
    ('AquaFlask Bottle', 'Rich Kids Water Bottle', '5.png', 1200);
