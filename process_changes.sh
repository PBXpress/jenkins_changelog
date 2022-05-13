#!/bin/sh

set -e
set -o pipefail
set -x

_MDIR="`realpath ${0}`"
MDIR="`dirname ${_MDIR}`"

CL_DIR_FP="${WORKSPACE}/${CL_DIR}"

rm -f "${WORKSPACE}/since_"*.html

find "${CL_DIR_FP}" -type f -name 'changelog*.xml' | xargs python3.8 ${MDIR}/test.py
