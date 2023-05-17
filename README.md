# gh-actions


# Testing

Tests rely upon [act](https://github.com/nektos/act) for local validation

```
 act -s GITHUB_TOKEN="test"
 ```
\n# Integrations\n
## Snowflake

The Snowflake action depends on Snowflake's python connector library. 
You can find complete documentation about the library in the Snowflake docs [here](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector) with more detail about the connector [here](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-api).


### Snowflake Fields

| Field     | Value                                                                   | Example          |
| --------- | ----------------------------------------------------------------------- | ---------------- |
| account   | Snowflake account, the characters in front of `.snowflakecomputing.com` | hujwihs-hab96881 |
| user      | Database user                                                           |                  |
| role      | Snowflake role to use                                                   | READ_ONLY        |
| warehouse | Snowflake warehouse to use                                              | COMPUTE_WH       |
| database  | Snowflake database                                                      |                  |
| schema    | Snowflake schema to use (optional)                                      |                  |
| password  | Database password                                                       |                  |
\n
## Redshift

The Redshift action depends on Amazon's python connector library. 
You can find complete documentation about the library in the AWS docs [here](https://github.com/aws/amazon-redshift-python-driver).


### Redshift Fields

| Field            | Value                                  | Example                      |
| ---------------- | -------------------------------------- | ---------------------------- |
| db-host          | Database host                          | www.your-domain.com          |
| db-port          | Database port                          | 5439                         |
| db-database-name | Database Name                          | grai                         |
| db-user          | Database user                          | grai                         |
| db-password      | Database password                      | grai                         |
\n
## Flat File

The flat file action reads a flat file like csv, parquet, or feather inside of your github project to perform tests and update your grai instance.
Because of this, it's critical your file is up to date on each pull request. 

Make sure to include an `- uses: actions/checkout@v3` step in your workflow so that your repo code is available.


## dbt Fields

| Field          | Value                                                                 | Example         |
| -------------- | --------------------------------------------------------------------- | --------------- |
| file           | The file location in your repository of the updated flat file         | data.csv        |
\n
## Microsoft SQL Server

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
\n
## BigQuery

The BigQuery action depends on Google's python BigQuery library. 
More information can be found about specific connection credentials in Google's documentation [here](https://cloud.google.com/python/docs/reference/bigquery/latest).


### BigQuery Fields

| Field       | Value                                                                 | Example         |
| ----------- | --------------------------------------------------------------------- | --------------- |
| project     | BigQuery project string                                               | my-project      |
| dataset     | BigQuery dataset string                                               | my-dataset      |
| credentials | A JSON credential string for use with google oauth service account [connections](https://google-auth.readthedocs.io/en/master/reference/google.oauth2.service_account.html#google.oauth2.service_account.Credentials)                  |       |
\n
## Postgres

The Postgres action depends on the python psycopg2 library. 
You can find complete documentation about the library [here](https://www.psycopg.org/docs/).


### Fields

| Field            | Value                                  | Example                      |
| ---------------- | -------------------------------------- | ---------------------------- |
| db-host          | Database host                          | www.your-domain.com          |
| db-port          | Database port                          | 5432                         |
| db-database-name | Database Name                          | grai                         |
| db-user          | Database user                          | grai                         |
| db-password      | Database password                      | grai                         |
\n
## Fivetran

The Fivetran Action relies upon access to Fivetran's API endpoint. 
This endpoint is configurable if you have a non-standard implementation but should generally be left alone.

Authentication with their services will require an API key and secret but you can find more documentation about generating these values [here](https://fivetran.com/docs/rest-api/getting-started#instructions).

### Fields

| Field             | Value                                  | Example                      |
| ----------------- | -------------------------------------- | ---------------------------- |
| fivetran_endpoint | Optional, fivetran url endpoint        | https://api.fivetran.com/v1  |
| api_key           | Fivetran user API key                  |                              |
| api_secret        | Fivetran user API secret               |                              |
| namespace_map     | Optional JSON string                   | See below                    |


The `namespace` field in the Fivetran Action works slightly differently than other action.
It is used as a default namespace for all connections not specified in the `namespace_map`. 
You can find more information about that below.


#### Namespace Map

Each Fivetran connection has a connector id and synchronizes from a source to a sync. 
For example, a sync from your production database to data warehouse would have an associated connector id.

Because the Fivetran Action synchronizes from all of your Fivetran connections it uses the `namespace_map` value to know which connectors belong to which Grai namespaces.
The namespace map should be a JSON string with the Grai namespace for each source and destination of each connector id e.g.

```json
{
    "<connector_id>": {
        "source": "<source_namespace>",
        "destination", "<destination_namespace>"
    }
}



You can find connector id's for all of your Fivetran connections in the [API](https://fivetran.com/docs/rest-api/faq/find-connector_id)
\n
## MySQL 

The MySQL action depends on the python mysql library. 
You can find complete documentation about the library [here](https://dev.mysql.com/doc/connector-python).


### Fields

| Field            | Value                                  | Example                      |
| ---------------- | -------------------------------------- | ---------------------------- |
| db-host          | Database host                          | www.your-domain.com          |
| db-port          | Database port                          | 3306                         |
| db-database-name | Database Name                          | grai                         |
| db-user          | Database user                          | grai                         |
| db-password      | Database password                      | grai                         |
\n
## dbt

The dbt action reads a manifest.json file inside of your github project to perform tests and update your grai instance.
Because of this, it's critical your manifest.json file is up to date on each pull request. 
One way to do this is to perform `dbt build` as part of your CI action but there are multiple ways to generate an up-to-date manifest file.

* More information about manifest.json files can be found [here](https://docs.getdbt.com/reference/artifacts/manifest-json).
* Make sure to include an `- uses: actions/checkout@v3` step in your workflow so that your repo code is available.



### dbt Fields

| Field         | Value                                                                 | Example         |
| --------------| --------------------------------------------------------------------- | --------------- |
| manifest-file | The file location in your repository of the updated manifest.json     | profile-dir/manifest.json      |
\n
