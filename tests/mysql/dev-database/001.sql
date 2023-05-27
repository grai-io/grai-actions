CREATE TABLE dbo.customers(
	id int NOT NULL AUTO_INCREMENT,
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	created_at DATETIME NOT NULL,
    PRIMARY KEY ( id )
);