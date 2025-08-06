#!/usr/bin/env bash

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

find "$SCRIPT_DIR"/.. -name README.py -exec "$SCRIPT_DIR"/jupytext_py_to_notebook.sh {} \;
