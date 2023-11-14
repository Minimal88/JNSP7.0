#!/bin/bash

# usage
function usage(){
	

cat<<EOF
	
USAGE: $0 GLAB_OUTS_FILES"


EOF
	
	
	exit 0
	
}

	
#
function filter_outs()
{

	grep ^SBASOUT  "${fout}" > "${fpos}"
	grep ^SBASCORR "${fout}" > "${fcor}"
	grep ^SBASVAR  "${fout}" > "${fvar}"
	grep ^SBASIONO "${fout}" > "${fion}"
	grep ^FILTER "${fout}" > "${ffil}"
	grep ^MODEL "${fout}" > "${fmod}"
	grep ^MEAS "${fout}" > "${fmeas}"
	grep ^EPOCHSAT "${fout}" > "${fsat}"
	grep ^OUTPUT "${fout}" > "${foutput}"

}
	

#
function define_files_names(){
	
	fpos=$(basename "${fout}" .out).pos
	fcor=$(basename "${fout}" .out).cor
	fvar=$(basename "${fout}" .out).var
	fion=$(basename "${fout}" .out).ion
	fmod=$(basename "${fout}" .out).model
	ffil=$(basename "${fout}" .out).filter
	fmeas=$(basename "${fout}" .out).meas
	fsat=$(basename "${fout}" .out).sat
	foutput=$(basename "${fout}" .out).output
	

}

#----------------------------------------------------------------------
# MAIN PROCESSING
#----------------------------------------------------------------------

# Check input arguments
[ $# -eq 0 ] && usage

# Input Argument
FOUTFILES=$*

# Loop over all the Observation files
for fout in ${FOUTFILES}
do

echo "[INFO]: Filtering file ${fout}..."

# Define files name
define_files_names

# Filter GLAB Outputs
filter_outs

done




