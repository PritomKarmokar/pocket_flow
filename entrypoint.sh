#!/bin/bash

# Section 01: Bash Options
set -o errexit
set -o pipefail
set -o nounset

# Section 02: Health of dependent Service
postgres_ready(){
    python3 << END
import sys
from psycopg2 import connect
from psycopg2.errors import OperationalError

try:
    connect(
        dbname="${DB_NAME}",
        user="${DB_USER}",
        password="${DB_PASSWORD}",
        host="${DB_HOST}",
        port="${DB_PORT}",
    )
except OperationalError:
    sys.exit(-1)
END
}

until postgres_ready; do
    >&2 echo "Waiting for PostgreSQL to become available..."
    sleep 5
done
>&2 echo "PostgreSQL is available"

# Section 03: Idempotent Django commands
python3 manage.py collectstatic --noinput
python3 manage.py makemigrations
python3 manage.py migrate

exec "$@"