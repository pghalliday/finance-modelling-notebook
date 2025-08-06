#!/usr/bin/env bash

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

"$SCRIPT_DIR"/scripts/convert_readme_notebooks.sh
"$SCRIPT_DIR"/scripts/jupytext_notebooks_to_py.sh
