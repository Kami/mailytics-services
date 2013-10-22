#!/usr/bin/env bash

BASEDIR=`dirname $0`
DATE=$(date +%s)
DB_FILE=${1:-"database.sqlite"}
BACKUP_FILE=${2:-"backup-$DATE.sql"}

if [ ! -f ${DB_FILE} ]; then
    echo "Database doesn't exist, skipping backup"
    exit 0
fi

sqlite3 ${DB_FILE} .dump > ${BACKUP_FILE}.sql
