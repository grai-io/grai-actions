CREATE TABLE dbo.orders(
	id int NOT NULL AUTO_INCREMENT,
	user_id int NOT NULL,
	status text NOT NULL,
	order_date date NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES customers(id)
);