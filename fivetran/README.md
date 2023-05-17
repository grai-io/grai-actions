# Fivetran

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
```


You can find connector id's for all of your Fivetran connections in the [API](https://fivetran.com/docs/rest-api/faq/find-connector_id)


