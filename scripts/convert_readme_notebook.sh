#!/usr/bin/env bash

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

WORKING_DIR=$(realpath "$SCRIPT_DIR"/..)
NOTEBOOK_PATH=$(realpath "$1")

papermill --cwd "$WORKING_DIR" "$NOTEBOOK_PATH" "$NOTEBOOK_PATH"
jupyter nbconvert --to markdown "$NOTEBOOK_PATH"
