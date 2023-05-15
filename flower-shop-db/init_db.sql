CREATE TABLE customer
(
    customer_id SERIAL,
    email VARCHAR(50) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    CONSTRAINT PK_CUSTOMER PRIMARY KEY (customer_id)
);

CREATE TABLE vendor
(
    vendor_id SERIAL,
    email VARCHAR(50) NOT NULL UNIQUE,
    company_name VARCHAR(50) NOT NULL UNIQUE,
    company_address VARCHAR(100) NOT NULL,
    bank_account VARCHAR(34) NOT NULL,
    CONSTRAINT PK_VENDOR PRIMARY KEY (vendor_id)
);

CREATE TABLE product_category
(
    product_category_id SERIAL,
    product_category_name VARCHAR(50) NOT NULL UNIQUE,
    CONSTRAINT PK_PRODUCT_CATEGORY PRIMARY KEY (product_category_id)
);

CREATE TABLE product
(
    product_id SERIAL,
    vendor_id INT NOT NULL,
    product_category_id INT NOT NULL,
    product_name VARCHAR(50) NOT NULL,
    description VARCHAR(400) NOT NULL,
    price INT NOT NULL CHECK (price > 0),
    availability VARCHAR(50) NOT NULL CHECK (availability IN ('in stock', 'out of stock')),
    CONSTRAINT PK_PRODUCT PRIMARY KEY (product_id),
    CONSTRAINT FK_PRODUCT_VENDOR FOREIGN KEY (vendor_id) REFERENCES vendor (vendor_id) ON DELETE CASCADE,
    CONSTRAINT FK_PRODUCT_CATEGORY FOREIGN KEY (product_category_id) REFERENCES product_category (product_category_id) ON DELETE CASCADE,
    CONSTRAINT UK_PRODUCT UNIQUE (vendor_id, product_category_id, product_name)
);

CREATE TABLE tag
(
    tag_id SERIAL,
    tag_name VARCHAR(50) NOT NULL UNIQUE,
    CONSTRAINT PK_TAG PRIMARY KEY (tag_id)
);

CREATE TABLE product_tag
(
    product_id INT NOT NULL,
    tag_id INT NOT NULL,
    CONSTRAINT PK_PRODUCT_TAG PRIMARY KEY (product_id, tag_id),
    CONSTRAINT FK_TAG_PRODUCT FOREIGN KEY (product_id) REFERENCES product (product_id) ON DELETE CASCADE,
    CONSTRAINT FK_PRODUCT_TAG FOREIGN KEY (tag_id) REFERENCES tag (tag_id) ON DELETE CASCADE
);

CREATE TABLE cart
(
    cart_id SERIAL,
    customer_id INT NOT NULL,
    total_price INT DEFAULT 0,
    status VARCHAR(10) DEFAULT 'current' CHECK (status IN
    ('current', 'old')),
    CONSTRAINT PK_CART PRIMARY KEY (cart_id),
    CONSTRAINT FK_CART_CUSTOMER FOREIGN KEY (customer_id) REFERENCES customer (customer_id) ON DELETE CASCADE
);

CREATE TABLE cart_product
(
    cart_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    CONSTRAINT PK_CART_PRODUCT PRIMARY KEY (cart_id, product_id),
    CONSTRAINT FK_PRODUCT_CART FOREIGN KEY (cart_id) REFERENCES cart (cart_id) ON DELETE CASCADE,
    CONSTRAINT FK_CART_PRODUCT FOREIGN KEY (product_id) REFERENCES product (product_id) ON DELETE CASCADE
);

CREATE TABLE "order"
(
    order_id SERIAL,
    cart_id INT NOT NULL UNIQUE,
    order_date DATE NOT NULL,
    total_price INT DEFAULT 0,
    shipping_address VARCHAR(100) NOT NULL,
    customer_bank_account VARCHAR(34) NOT NULL,
    CONSTRAINT PK_ORDER PRIMARY KEY (order_id),
    CONSTRAINT FK_ORDER_CART FOREIGN KEY (cart_id) REFERENCES cart (cart_id) ON DELETE CASCADE
);
