# grai-actions


# Integrations

# Shared Fields

All actions share some common fields listed below.


### Authentication

| Field              | Required | Default             | Description                                                                                           |
|--------------------|----------|---------------------|-------------------------------------------------------------------------------------------------------|
| api-key            | no       |                     | Your Grai API key.                                                                                    |
| grai-user          | no       |                     | Your Gri username.                                                                                    |
| grai-password      | no       |                     | Your Gri password.                                                                                    |
| workspace          | no       |                     | Your Grai workspace name                                                                              |

You must provider either `api-key` or `grai-user` **and** `grai-password`.
If you're account is associated with multiple workspaces and you're using username/password authentication you must 
also provide your desired `workspace`.


### Other parameters

| Field              | Required | Default             | Description                                                                                           |
|--------------------|----------|---------------------|-------------------------------------------------------------------------------------------------------|
| namespace          | yes      |                     | The Grai namespace for the connection                                                                 |
| client-host        | no       | api.grai.io         | Hostname for the api of your Grai instance.                                                           |
| client-port        | no       |                     | Port for the api of your Grai Instance.                                                               |
| grai-frontend-host | no       | https://app.grai.io | The URL for your frontend instance of Grai. This might include a port depending on your configuration |
| action             | no       | tests               | Which action to perform. Can be `tests` or `update`                                                   |
| github-token       | no       | ${{ github.token }} | The GITHUB_TOKEN secret for your repository                                                           |


## Snowflake

The Snowflake action depends on Snowflake's python connector library. 
You can find complete documentation about the library in the Snowflake docs [here](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector) with more detail about the connector [here](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-api).


### Fields

<!-- Fields Sentinel Section -->
| Field | Required | Default | Description |
|-----|-----|-----|-----|
| db-user | yes |  | The database user |
| db-password | yes |  | The database password |
| account | yes |  | Associated Snowflake account |
| warehouse | yes |  | Associated Snowflake warehouse |
| role | no |  | Optional Snowflake role |
| database | no |  | Optional Snowflake database |
| schema | no |  | Optional snowflake schema |
<!-- Fields Sentinel Section -->















    
    
  
## Redshift

The Redshift action depends on Amazon's python connector library. 
You can find complete documentation about the library in the AWS docs [here](https://github.com/aws/amazon-redshift-python-driver).


### Fields

<!-- Fields Sentinel Section -->
| Field | Required | Default | Description |
|-----|-----|-----|-----|
| db-host | yes |  | The database host |
| db-port | no | 5439 | The database port |
| db-database-name | yes |  | The database name |
| db-user | yes |  | The database user |
| db-password | yes |  | The database password |
<!-- Fields Sentinel Section -->
  
## Flat File

The flat file action reads a flat file like csv, parquet, or feather inside of your github project to perform tests and update your grai instance.
Because of this, it's critical your file is up to date on each pull request. 

Make sure to include an `- uses: actions/checkout@v3` step in your workflow so that your repo code is available.


### Fields

<!-- Fields Sentinel Section -->
| Field | Required | Default | Description |
|-----|-----|-----|-----|
| file | yes |  | Local file to track with Grai |
<!-- Fields Sentinel Section -->
  
## Microsoft SQL Server

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
  
## BigQuery

The BigQuery action depends on Google's python BigQuery library. 
More information can be found about specific connection credentials in Google's documentation [here](https://cloud.google.com/python/docs/reference/bigquery/latest).


### Fields

<!-- Fields Sentinel Section -->
| Field | Required | Default | Description |
|-----|-----|-----|-----|
| project | yes |  | The BigQuery project string |
| dataset | yes |  | The BigQuery dataset string |
| credentials | yes |  | A JSON credential string for use with google oauth service account [connections](https://google-auth.readthedocs.io/en/master/reference/google.oauth2.service_account.html#google.oauth2.service_account.Credentials) |
<!-- Fields Sentinel Section -->
  
## Postgres

The Postgres action depends on the python psycopg2 library. 
You can find complete documentation about the library [here](https://www.psycopg.org/docs/).


### Fields

<!-- Fields Sentinel Section -->
| Field | Required | Default | Description |
|-----|-----|-----|-----|
| db-host | yes |  | The database host |
| db-port | no | 5432 | The database port |
| db-database-name | yes |  | The database name |
| db-user | yes |  | The database user |
| db-password | yes |  | The database password |
<!-- Fields Sentinel Section -->
  
## Fivetran

The Fivetran Action relies upon access to Fivetran's API endpoint. 
This endpoint is configurable if you have a non-standard implementation but should generally be left alone.

Authentication with their services will require an API key and secret but you can find more documentation about generating these values [here](https://fivetran.com/docs/rest-api/getting-started#instructions).

### Fields

<!-- Fields Sentinel Section -->
| Field | Required | Default | Description |
|-----|-----|-----|-----|
| fivetran-endpoint | no | https://api.fivetran.com/v1 | Fivetran API endpoint |
| fivetran-api-key | yes |  | Your Fivetran user api key |
| fivetran-api-secret | yes |  | Your Fivetran user api secret |
| namespace-map | no |  | A JSON string containing a mapping between Fivetran connections and Grai namespaces |
<!-- Fields Sentinel Section -->


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
```


You can find connector id's for all of your Fivetran connections in the [API](https://fivetran.com/docs/rest-api/faq/find-connector_id)
  
## MySQL 

The MySQL action depends on the python mysql library. 
You can find complete documentation about the library [here](https://dev.mysql.com/doc/connector-python).


### Fields

<!-- Fields Sentinel Section -->
| Field | Required | Default | Description |
|-----|-----|-----|-----|
| db-host | yes |  | The database host |
| db-port | no | 3306 | The database port |
| db-database-name | yes |  | The database name |
| db-user | yes |  | The database user |
| db-password | yes |  | The database password |
<!-- Fields Sentinel Section -->
  
## dbt

The dbt action reads a manifest.json file inside of your github project to perform tests and update your grai instance.
Because of this, it's critical your manifest.json file is up to date on each pull request. 
One way to do this is to perform `dbt build` as part of your CI action but there are multiple ways to generate an up-to-date manifest file.

* More information about manifest.json files can be found [here](https://docs.getdbt.com/reference/artifacts/manifest-json).
* Make sure to include an `- uses: actions/checkout@v3` step in your workflow so that your repo code is available.



### Fields

<!-- Fields Sentinel Section -->
| Field | Required | Default | Description |
|-----|-----|-----|-----|
| manifest-file | yes |  | The file location in your repository of the updated manifest.json file |
<!-- Fields Sentinel Section -->
  
