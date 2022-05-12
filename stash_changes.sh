#!/bin/sh

set -e
set -o pipefail
#set -x

CL_DIR_FP="${WORKSPACE}/${CL_DIR}"
CL_DIR_PT="${CL_DIR_FP%.*}"

rm -rf "${CL_DIR_PT}."*
mkdir "${CL_DIR_FP}"

for file in `find ${JENKINS_HOME}/jobs -type f -name 'changelog*.xml' ! -empty`
 do
   cp "${file}" "${CL_DIR_FP}/"
 done
