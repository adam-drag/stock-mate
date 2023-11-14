CREATE SCHEMA IF NOT EXISTS stock_management;

CREATE TABLE IF NOT EXISTS stock_management.product (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    safety_stock INT,
    max_stock INT,
    quantity INT
);

CREATE TABLE IF NOT EXISTS stock_management.supplier (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS stock_management.product_supplier (
    product_id VARCHAR(20),
    supplier_id VARCHAR(20),
    price DECIMAL(10, 2),
    lead_time INT,
    incoterms_2020 VARCHAR(255),
    FOREIGN KEY (product_id) REFERENCES stock_management.product(id),
    FOREIGN KEY (supplier_id) REFERENCES stock_management.supplier(id),
    PRIMARY KEY (product_id, supplier_id)
);

CREATE TABLE IF NOT EXISTS stock_management.customer (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT
);

CREATE TABLE IF NOT EXISTS stock_management.purchase_order_header (
    id VARCHAR(20) PRIMARY KEY,
    supplier_id VARCHAR(20),
    order_date DATE,
    delivery_date DATE,
    FOREIGN KEY (supplier_id) REFERENCES stock_management.supplier(id)
);

CREATE TABLE IF NOT EXISTS stock_management.purchase_order_position (
    id VARCHAR(20) PRIMARY KEY,
    product_id VARCHAR(20),
    purchase_order_header_id VARCHAR(20),
    quantity_ordered INT,
    quantity_received INT,
    price DECIMAL(10, 2),
    FOREIGN KEY (product_id) REFERENCES stock_management.product(id),
    FOREIGN KEY (purchase_order_header_id) REFERENCES stock_management.purchase_order_header(id)
);

CREATE TABLE IF NOT EXISTS stock_management.sales_order_header (
    id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20),
    order_date DATE,
    delivery_date DATE,
    FOREIGN KEY (customer_id) REFERENCES stock_management.customer(id)
);

CREATE TABLE IF NOT EXISTS stock_management.sales_order_position (
    id VARCHAR(20) PRIMARY KEY,
    product_id VARCHAR(20),
    sales_order_header_id VARCHAR(20),
    quantity_ordered INT,
    quantity_received INT,
    price DECIMAL(10, 2),
    FOREIGN KEY (product_id) REFERENCES stock_management.product(id),
    FOREIGN KEY (sales_order_header_id) REFERENCES stock_management.sales_order_header(id)
);

CREATE TABLE IF NOT EXISTS stock_management.usage (
    id VARCHAR(20) PRIMARY KEY,
    product_id VARCHAR(20),
    date DATE,
    quantity INT,
    FOREIGN KEY (product_id) REFERENCES stock_management.product(id)
);

CREATE TABLE IF NOT EXISTS stock_management.issue (
    id VARCHAR(20) PRIMARY KEY,
    type VARCHAR(50),
    action VARCHAR(50),
    severity VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS stock_management.events (
    event_id VARCHAR(20) PRIMARY KEY,
    event_type VARCHAR(255),
    emitter VARCHAR(255),
    message TEXT,
    created_at TIMESTAMP
);
