#!/usr/bin/env bash

DB_FILE=${1:-"database.sqlite"}

sqlite3 ${DB_FILE} < fixtures/schema.sql
