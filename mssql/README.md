# Microsoft SQL Server

The SQL Server action depends on the python pyodbc library. 
You can find complete documentation about the library [here](https://github.com/mkleehammer/pyodbc/wiki).

There are a variety of ways to configure a pyodbc connection depending on your security implementation.
A standard connection would consist of a host, port, database name, user, and password.

### Fields

<!-- Fields Sentinel Section -->
| Field | Required | Default | Description |
|-----|-----|-----|-----|
| db-host | no |  | The MSSQL database host |
| db-port | no | 1433 | The MSSQL database port. |
| db-database-name | no |  | The database name |
| db-user | no | sa | The database user |
| db-password | no |  | The database password |
| encrypt | no |  | True/False Indicates whether to use an encrypted connection to mssql |
| trusted_connection | no |  | True/False whether the SQL Server connection is trusted. Sets `Trusted_Connection=yes` in pyodbc. |
| protocol | no | tcp | Connection protocol for the database. One of 'tcp', 'Icp', or 'NP' |
| server_connection_string | no |  | An optional ODBC server connection string to use when connecting to the server. These are usually constructed as '{protocol}:{host},{port}'. This |
| trust_server_certificate | no | true | Sets the ODBC connection string `TrustServerCertificate` |
<!-- Fields Sentinel Section -->


