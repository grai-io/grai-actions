# Flat File

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
          source-name: prod-db
          grai-api-url: https://api.grai.io
          file: ./tests/flat-file/low-numbers.csv

```

<!-- Example Sentinel Section -->

