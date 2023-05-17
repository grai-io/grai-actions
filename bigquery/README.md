# BigQuery

The BigQuery action depends on Google's python BigQuery library. 
More information can be found about specific connection credentials in Google's documentation [here](https://cloud.google.com/python/docs/reference/bigquery/latest).


### BigQuery Fields

| Field       | Value                                                                 | Example         |
| ----------- | --------------------------------------------------------------------- | --------------- |
| project     | BigQuery project string                                               | my-project      |
| dataset     | BigQuery dataset string                                               | my-dataset      |
| credentials | A JSON credential string for use with google oauth service account [connections](https://google-auth.readthedocs.io/en/master/reference/google.oauth2.service_account.html#google.oauth2.service_account.Credentials)                  |       |
