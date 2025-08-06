#!/usr/bin/env bash

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

WORKING_DIR=$(realpath "$SCRIPT_DIR"/..)
INPUT=$(realpath "$1")

papermill --cwd "$WORKING_DIR" "$INPUT" "$INPUT"
jupyter nbconvert --to markdown "$INPUT"
