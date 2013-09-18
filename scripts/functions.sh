#!/usr/bin/env bash

function die_on_non_zero() {
  if [ $? -ne 0 ]; then
     echo $1;
     exit 1;
  fi
}
