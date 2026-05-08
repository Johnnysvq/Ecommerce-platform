-- Tabla de productos
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price DECIMAL(10,2),
    description TEXT,
    category VARCHAR(100),
    image VARCHAR(500),
    rating_rate DECIMAL(3,1),
    rating_count INTEGER,
    loaded_at TIMESTAMP
);

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    email VARCHAR(255),
    username VARCHAR(100),
    password VARCHAR(255),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    full_name VARCHAR(200),
    city VARCHAR(100),
    country VARCHAR(255),
    zipcode VARCHAR(20),
    geo_lat DECIMAL(10,6),
    geo_lng DECIMAL(10,6),
    phone VARCHAR(50),
    loaded_at TIMESTAMP
);

-- Tabla de ordenes
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    order_id INTEGER,
    user_id INTEGER,
    order_date TIMESTAMP,
    product_id INTEGER,
    quantity INTEGER,
    loaded_at TIMESTAMP
);