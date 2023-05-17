# gh-actions


# Testing

Tests rely upon [act](https://github.com/nektos/act) for local validation

```
 act -s GITHUB_TOKEN="test"
 ```

# Integrations

## Fivetran


## Flat File


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


## BigQuery

The BigQuery action depends on Google's python BigQuery library. 
More information can be found about specific connection credentials in Google's documentation [here](https://cloud.google.com/python/docs/reference/bigquery/latest).


### BigQuery Fields

| Field       | Value                                                                 | Example         |
| ----------- | --------------------------------------------------------------------- | --------------- |
| project     | BigQuery project string                                               | my-project      |
| dataset     | BigQuery dataset string                                               | my-dataset      |
| credentials | A JSON credential string for use with google oauth service account [connections](https://google-auth.readthedocs.io/en/master/reference/google.oauth2.service_account.html#google.oauth2.service_account.Credentials)                  |       |


## Snowflake


## Redshift


## Postgres


## MySQL 


## Microsoft SQL Server


