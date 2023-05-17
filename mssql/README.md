# Microsoft SQL Server

The SQL Server action depends on the python pyodbc library. 
You can find complete documentation about the library [here](https://github.com/mkleehammer/pyodbc/wiki).

There are a variety of ways to configure a pyodbc connection depending on your security implementation.
A standard connection would consist of a host, port, database name, user, and password.

### Fields

| Field     | Value                                               | Example              |
| --------- | --------------------------------------------------- | -------------------- |
| db-host      | Database host                                    | www.your-domain.com  |
| db-port      | Database port                                    | 1433                 |
| db-database-name  | Database name                               | jaffle_shop          |
| db-user      | Database user                                    | grai                 |
| db-password  | Database password                                | grai                 |
| encrypt   | A boolean value indicating whether to use an encrypted connection to mssql | True    |
| trusted_connection  | Boolean, sets `Trusted_Connection=yes` in pyodbc      | False     |
| protocol | Optional, One of "tcp", "Icp", or "NP". Defaults to "tcp"        | tcp       |
| server_connection_string  | Server connection string for pyodbc, Sets `Server={VALUE}` | grai      |
| trust_server_certificate | Boolean, sets the `TrustServerCertificate` value in pyodbc  | grai      |
