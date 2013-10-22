#!/usr/bin/env bash

BASEDIR=`dirname $0`
DB_FILE=${1:-"database.sqlite"}

sqlite3 ${DB_FILE} < ${BASEDIR}/../fixtures/schema.sql
