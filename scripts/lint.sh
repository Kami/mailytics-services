#!/usr/bin/env bash

source ./scripts/functions.sh

flake8 $(find ./token_storage_client ./token_storage_server ./tests -type f -name "*.py")
die_on_non_zero "flake8 failed"
