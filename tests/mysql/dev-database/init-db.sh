SCRIPT_DIR=$(dirname -- "$0")
host="${GRAI_DB_HOST:-localhost}"
port="${GRAI_DB_PORT:-3306}"
user="${GRAI_DB_USER:-grai}"
password="${GRAI_DB_PASSWORD:-grai}"
database="${GRAI_DB_DATABASE_NAME:-grai}"

for file in $(find $SCRIPT_DIR -type f -name '*.sql' | sort)
do
  echo "Executing $file"
  mysql -u $user --password=$password -h $host --protocol=TCP $database < $file
done

