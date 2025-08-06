#!/usr/bin/env bash

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

find "$SCRIPT_DIR"/.. -name README.ipynb -exec "$SCRIPT_DIR"/convert_readme_notebook.sh {} \;
