# Grai Actions


## Shared Fields

All actions share some common fields listed below.


### Authentication

| Field              | Required | Default             | Description              |
|--------------------|----------|---------------------|--------------------------|
| api-key            | no       |                     | Your Grai API key.       |
| grai-user          | no       |                     | Your Grai username.      |
| grai-password      | no       |                     | Your Grai password.      |
| workspace          | no       |                     | Your Grai workspace name |

You must provider either `api-key` or `grai-user` **and** `grai-password`.
If you're account is associated with multiple workspaces and you're using username/password authentication you must 
also provide your desired `workspace`.


### Other Parameters

| Field          | Required | Default             | Description                                                                                                 |
|----------------|----------|---------------------|-------------------------------------------------------------------------------------------------------------|
| namespace      | yes      |                     | The Grai namespace for the connection                                                                       |
| grai-api-url   | no       | https://api.grai.io | "The url of your grai instance. This is constructed as {scheme}://{host}:{port} where the port is optional" |
| grai-app-url   | no       | https://app.grai.io | The URL for your frontend instance of Grai. This might include a port depending on your configuration       |
| action         | no       | tests               | Which action to perform. Can be `tests` or `update`                                                         |
| github-token   | no       | `${{github.token}}` | The GITHUB_TOKEN secret for your repository                                                                 |


## Notes and Caveats

### Github Authentication

By default we use a `github-token` provided by your repository to write comments back to your PR with test results. 
In some cases, such as when the pull request is coming from a forked repository, the default token will not have write 
permissions.
If this is the case, you'll receive an error message in the workflow indicating such.
There are a few ways you can resolve the issue but you should first check your repository action settings under
`Settings -> Actions -> General` aren't blocking workflows from running.


Some alternatives include.

#### Explicit Workflow Permissions

GitHub has provided helpful [documentation](https://docs.github.com/en/actions/using-jobs/assigning-permissions-to-jobs)
to provide explicit permissions for your workflows. 
Make sure the Grai Action has, at minimum, write permissions for `pull-request` and `issues`. 
You can set this at the job level by adding a `permission` key in your workflow. e.g.

```yaml copy
jobs:
  my-grai-action:
    runs-on: ubuntu-latest

    permissions:
      issues: write
      pull-requests: write

```

#### Personal Access Tokens

You can also use personal access tokens or [PAT](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)'s
in place of the default github-token.
You'll need to create a token following the linked instructions but make sure to store it in your repository secrets
`Settings -> Secrets and variables -> Actions -> New Repository Secret`.
If you were to create a secret called `MY_PAT` you would pass it into your grai action job as

````yaml copy
jobs:
  my-grai-action:
    runs-on: ubuntu-latest
  
  steps:
    - name: Checkout
      uses: actions/checkout@v3
      
    - name: Run Grai Action
      uses: grai-io/grai-actions/redshift@master
      with:
        github-token: ${{ secrets.MY_PAT }}
````

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

### Example

<!-- Example Sentinel Section -->

```yaml copy
on:
  - pull_request
name: Fivetran
jobs:
  test_fivetran:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Run Grai Action
        uses: grai-io/grai-actions/fivetran@master
        with:
          namespace: my_apps_grai_namespace
          api-key: my_grai_api_key
          action: tests
          grai-api-url: https://api.grai.io
          fivetran-api-key: hHqP5c2nIY0B6fpa
          fivetran-api-secret: 1234567890abcdef1234567890abcdef
          namespace-map: '{"operative_combination": {"source": "source_namespace",
            "destination": "destination_namespace"}}'

```

<!-- Example Sentinel Section -->
  
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

### Example

<!-- Example Sentinel Section -->

```yaml copy
on:
  - pull_request
name: Flat File
jobs:
  test_flat-file:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Run Grai Action
        uses: grai-io/grai-actions/flat-file@master
        with:
          namespace: my_apps_grai_namespace
          api-key: my_grai_api_key
          action: tests
          grai-api-url: https://api.grai.io
          file: ./tests/flat-file/low-numbers.csv

```

<!-- Example Sentinel Section -->
  
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

### Example

<!-- Example Sentinel Section -->

```yaml copy
on:
  - pull_request
name: Snowflake
jobs:
  test_snowflake:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Run Grai Action
        uses: grai-io/grai-actions/snowflake@master
        with:
          namespace: my_apps_grai_namespace
          api-key: my_grai_api_key
          action: tests
          grai-api-url: https://api.grai.io
          db-user: my-user
          db-password: my-password
          account: my-account
          warehouse: my-warehouse

```

<!-- Example Sentinel Section -->
  
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

### Example

<!-- Example Sentinel Section -->

```yaml copy
on:
  - pull_request
name: PostgreSQL
jobs:
  test_postgres:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Run Grai Action
        uses: grai-io/grai-actions/postgres@master
        with:
          namespace: my_apps_grai_namespace
          api-key: my_grai_api_key
          action: tests
          grai-api-url: https://api.grai.io
          db-host: prod.db.com
          db-port: '5432'
          db-database-name: my_database
          db-user: my_user
          db-password: my_password

```

<!-- Example Sentinel Section -->
  
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

### Example

<!-- Example Sentinel Section -->

```yaml copy
on:
  - pull_request
name: BigQuery
jobs:
  test_bigquery:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Run Grai Action
        uses: grai-io/grai-actions/bigquery@master
        with:
          namespace: my_apps_grai_namespace
          api-key: my_grai_api_key
          action: tests
          grai-api-url: https://api.grai.io
          project: my-bigquery-project
          dataset: my-bigquery-dataset
          credentials: '{ "type": "service_account", "project_id": "demo", "private_key_id":
            "your_private_key_id", "private_key": "your_private_key", "client_email":
            "your@email.iam.gserviceaccount.com", "client_id": "your_client_id", "auth_uri":
            "https://accounts.google.com/o/oauth2/auth", "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/you%40email.iam.gserviceaccount.com"
            }'

```

<!-- Example Sentinel Section -->
  
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

### Example

<!-- Example Sentinel Section -->

```yaml copy
on:
  - pull_request
name: dbt
jobs:
  test_dbt:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Run Grai Action
        uses: grai-io/grai-actions/dbt@master
        with:
          namespace: my_apps_grai_namespace
          api-key: my_grai_api_key
          action: tests
          grai-api-url: https://api.grai.io
          manifest-file: ./tests/dbt/manifest.json

```

<!-- Example Sentinel Section -->
  
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
| server_connection_string | no |  | An optional ODBC server connection string to use when connecting to the server. These are usually constructed as `{protocol}:{host},{port}`. This |
| trust_server_certificate | no | true | Sets the ODBC connection string `TrustServerCertificate` |


<!-- Fields Sentinel Section -->

### Example

<!-- Example Sentinel Section -->

```yaml copy
on:
  - pull_request
name: SQL Server
jobs:
  test_mssql:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Run Grai Action
        uses: grai-io/grai-actions/mssql@master
        with:
          namespace: my_apps_grai_namespace
          api-key: my_grai_api_key
          action: tests
          grai-api-url: https://api.grai.io
          db-user: sa
          db-password: sa_password
          server_connection_string: tcp:myserver,1433
          trust_server_certificate: 'true'

```

<!-- Example Sentinel Section -->
  
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

### Example

<!-- Example Sentinel Section -->

```yaml copy
on:
  - pull_request
name: Redshift
jobs:
  test_redshift:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Run Grai Action
        uses: grai-io/grai-actions/redshift@master
        with:
          namespace: my_apps_grai_namespace
          api-key: my_grai_api_key
          action: tests
          grai-api-url: https://api.grai.io
          db-host: redshift-cluster-1.abc123xyz789.us-east-1.redshift.amazonaws.com
          db-port: '5439'
          db-database-name: dev
          db-user: admin
          db-password: password

```

<!-- Example Sentinel Section -->
  
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

### Example

<!-- Example Sentinel Section -->

```yaml copy
on:
  - pull_request
name: MySQL
jobs:
  test_mysql:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Run Grai Action
        uses: grai-io/grai-actions/mysql@master
        with:
          namespace: my_apps_grai_namespace
          api-key: my_grai_api_key
          action: tests
          grai-api-url: https://api.grai.io
          db-host: dev.mysql.com
          db-port: '3306'
          db-database-name: my_db
          db-user: my_user
          db-password: my_password

```

<!-- Example Sentinel Section -->
  
