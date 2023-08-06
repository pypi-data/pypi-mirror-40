#! /bin/sh
set -x
BACKUP_DIR=${BACKUP_DIR:=/tmp}
# DB_SERVER="127.0.0.1"
# DB_PORT="5423"
DB_USER="keycloak"
# DB_PASS="keycloak"

docker exec -it keycloak_db pg_dump --username=keycloak keycloak > $BACKUP_DIR/postgresqldump.sql
