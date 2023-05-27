CREATE TABLE dbo.payments(
	id int NOT NULL AUTO_INCREMENT,
	order_id int NOT NULL,
	payment_method text NOT NULL,
	amount int NULL,
	PRIMARY KEY (id),
    FOREIGN KEY (order_id) REFERENCES orders(id)
);