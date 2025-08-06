#!/usr/bin/env bash

set -e

NOTEBOOK_PATH=$(realpath "$1")

jupytext --to py "$NOTEBOOK_PATH"
