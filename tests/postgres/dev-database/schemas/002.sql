DROP TABLE IF EXISTS db.orders;

CREATE TABLE db.orders(
    id int NOT NULL PRIMARY KEY,
    user_id int NOT NULL,
    status text NOT NULL,
    order_date timestamp NOT NULL
    CONSTRAINT fk_customers
       FOREIGN KEY(user_id)
        REFERENCES db.customers(id)
);
