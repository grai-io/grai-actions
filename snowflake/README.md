# Snowflake

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