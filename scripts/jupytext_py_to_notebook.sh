#!/usr/bin/env bash

set -e

PY_PATH=$(realpath "$1")

jupytext --to notebook "$PY_PATH"
