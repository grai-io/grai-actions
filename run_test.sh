docker compose -f tests/postgres/docker-compose.yml up -d
docker compose -f tests/mysql/docker-compose.yml up -d
docker compose -f tests/mssql/docker-compose.yml up -d

act -j test_postgres_local -e ./actrc
act -j test_mysql_local -e ./actrc
act -j test_mssql_local -e ./actrc
act -j test_dbt_local -e ./actrc
act -j test_flat_file_local -e ./actrc
act -j test_redshift_local --env-file ./tests/redshift/.env -e ./actrc
act -j test_fivetran_local --env-file ./tests/fivetran/.env -e ./actrc
act -j test_bigquery_local --env-file ./tests/bigquery/.env -e ./actrc

docker compose -f tests/postgres/docker-compose.yml down
docker compose -f tests/mysql/docker-compose.yml down
docker compose -f tests/mssql/docker-compose.yml down