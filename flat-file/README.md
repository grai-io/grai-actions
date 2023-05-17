# Flat File

The flat file action reads a flat file like csv, parquet, or feather inside of your github project to perform tests and update your grai instance.
Because of this, it's critical your file is up to date on each pull request. 

Make sure to include an `- uses: actions/checkout@v3` step in your workflow so that your repo code is available.


## dbt Fields

| Field          | Value                                                                 | Example         |
| -------------- | --------------------------------------------------------------------- | --------------- |
| file           | The file location in your repository of the updated flat file         | data.csv        |

