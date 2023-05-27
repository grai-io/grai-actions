SCRIPT_DIR=$(dirname -- "$0")
host="${DB_HOST:-localhost}"
port="${DB_PORT:-3306}"
user="${DB_USER:-grai}"
password="${DB_PASSWORD:-grai}"
database="${DB_DATABASE_NAME:-grai}"

for file in $(find $SCRIPT_DIR -type f -name '*.sql' | sort)
do
  echo "Executing $file"
  mysql -u $user --password=$password -h $host --protocol=TCP $database < $file
done

