CREATE SCHEMA IF NOT EXISTS db;
DROP TABLE IF EXISTS db.customers;

CREATE TABLE db.customers(
    id INT NOT NULL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    created_at timestamp NOT NULL
);