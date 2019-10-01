#!/bin/bash

# make build ENV=$2

make build ENV=$2

NEWFILE=$(ls -t $1/dist/*.zip | head -1 | sed 's/.* dist\///')

echo "${NEWFILE}"

mv "${NEWFILE}" "builtSource.zip"

