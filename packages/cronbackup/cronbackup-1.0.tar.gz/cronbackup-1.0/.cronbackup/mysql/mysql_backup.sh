#! /bin/sh
set -x
BACKUP_DIR=${BACKUP_DIR:=/tmp}
DB_SERVER="127.0.0.1"
DB_PORT="13306"
DB_USER="root"
DB_PASS="abc123"

mysqldump --all-databases  --lock-tables=0 -h$DB_SERVER -P$DB_PORT -u$DB_USER -p$DB_PASS > $BACKUP_DIR/mysqldump.sql
