-- FOR USERS TABLE

CREATE OR REPLACE PROCEDURE create_user (
    in_username TEXT,
    in_password TEXT,
    in_fname TEXT,
    in_mname TEXT,
    in_lname TEXT,
    in_phone_number TEXT,
    in_image_filename TEXT,
    in_account_type TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO users (
        username,
        password,
        fname,
        mname,
        lname,
        phone_number,
        image_filename,
        account_type
    ) VALUES (
        in_username,
        in_password,
        in_fname,
        in_mname,
        in_lname,
        in_phone_number,
        in_image_filename,
        in_account_type
    );
END;
$$;

CREATE OR REPLACE PROCEDURE get_user (
    in_user_id INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT * FROM users WHERE id = in_user_id;
END;
$$;

CREATE OR REPLACE PROCEDURE update_user (
    in_user_id INTEGER,
    in_username TEXT,
    in_password TEXT,
    in_fname TEXT,
    in_mname TEXT,
    in_lname TEXT,
    in_phone_number TEXT,
    in_image_filename TEXT,
    in_account_type TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE users SET 
        username = in_username,
        password = in_password,
        fname = in_fname,
        mname = in_mname,
        lname = in_lname,
        phone_number = in_phone_number,
        image_filename = in_image_filename,
        account_type = in_account_type
    WHERE id = in_user_id;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_user (
    in_user_id INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM users WHERE id = in_user_id;
END;
$$;

-- FOR user-address table

CREATE OR REPLACE PROCEDURE create_user_address (
    in_user_id INTEGER,
    in_street TEXT,
    in_city TEXT,
    in_house_no TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO user_address (
        user_id,
        street,
        city,
        house_no
    ) VALUES (
        in_user_id,
        in_street,
        in_city,
        in_house_no
    );
END;
$$;

CREATE OR REPLACE PROCEDURE get_user_address (
    in_user_id INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT * FROM user_address WHERE user_id = in_user_id;
END;
$$;

CREATE OR REPLACE PROCEDURE update_user_address (
    in_user_address_id INTEGER,
    in_street TEXT,
    in_city TEXT,
    in_house_no TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE user_address SET 
        street = in_street,
        city = in_city,
        house_no = in_house_no
    WHERE id = in_user_address_id;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_user_address (
    in_user_address_id INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM user_address WHERE id = in_user_address_id;
END;
$$;

-- FOR PRODUCTS TABLE

CREATE OR REPLACE PROCEDURE create_product (
    in_name TEXT,
    in_description TEXT,
    in_image_filename TEXT,
    in_price INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO products (
        name,
        description,
        image_filename,
        price
    ) VALUES (
        in_name,
        in_description,
        in_image_filename,
        in_price
    );
END;
$$;

CREATE OR REPLACE PROCEDURE get_product (
    in_product_id INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT * FROM products WHERE id = in_product_id;
END;
$$;

CREATE OR REPLACE PROCEDURE update_product (
    in_product_id INTEGER,
    in_name TEXT,
    in_description TEXT,
    in_image_filename TEXT,
    in_price INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE products SET 
        name = in_name,
        description = in_description,
        image_filename = in_image_filename,
        price = in_price
    WHERE id = in_product_id;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_product (
    in_product_id INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM products WHERE id = in_product_id;
END;
$$;

-- FOR ORDERS TABLE

CREATE OR REPLACE PROCEDURE create_order (
    in_customer_id INTEGER,
    in_product_id INTEGER,
    in_quantity INTEGER,
    in_total_price INTEGER,
    in_status TEXT,
    in_address INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO orders (
        customer_id,
        product_id,
        quantity,
        total_price,
        status,
        address
    ) VALUES (
        in_customer_id,
        in_product_id,
        in_quantity,
        in_total_price,
        in_status,
        in_address
    );
END;
$$;

CREATE OR REPLACE PROCEDURE get_order (
    in_order_id INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT * FROM orders WHERE id = in_order_id;
END;
$$;

CREATE OR REPLACE PROCEDURE update_order (
    in_order_id INTEGER,
    in_customer_id INTEGER,
    in_product_id INTEGER,
    in_quantity INTEGER,
    in_total_price INTEGER,
    in_status TEXT,
    in_address INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE orders SET 
        customer_id = in_customer_id,
        product_id = in_product_id,
        quantity = in_quantity,
        total_price = in_total_price,
        status = in_status,
        address = in_address
    WHERE id = in_order_id;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_order (
    in_order_id INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM orders WHERE id = in_order_id;
END;
$$;

-- FOR DELIVERIES TABLE

CREATE OR REPLACE PROCEDURE create_delivery (
    in_order_id INTEGER,
    in_worker_id INTEGER,
    in_status TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO deliveries (
        order_id,
        worker_id,
        status
    ) VALUES (
        in_order_id,
        in_worker_id,
        in_status
    );
END;
$$;

CREATE OR REPLACE PROCEDURE get_delivery (
    in_delivery_id INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT * FROM deliveries WHERE id = in_delivery_id;
END;
$$;

CREATE OR REPLACE PROCEDURE update_delivery (
    in_delivery_id INTEGER,
    in_order_id INTEGER,
    in_worker_id INTEGER,
    in_status TEXT,
    in_date_delivered TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE deliveries SET 
        order_id = in_order_id,
        worker_id = in_worker_id,
        status = in_status,
        date_delivered = in_date_delivered
    WHERE id = in_delivery_id;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_delivery (
    in_delivery_id INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM deliveries WHERE id = in_delivery_id;
END;
$$;


