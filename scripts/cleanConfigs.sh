#!/bin/bash

ECEL_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"

rm -rf "$ECEL_DIR"/core/*.json

for plugin in "$ECEL_DIR"/plugins/collectors/*; do
    if [ -d "$plugin" ]; then
        rm -rf "$plugin"/*.json
    fi
done
