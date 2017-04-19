#!/usr/bin/env bash
snoopy_filepath="$1"
output_path="$2"

#merge first
cat ${snoopy_filepath}/*.txt > ${snoopy_filepath}/merged
mkdir -p ${output_path}
java -cp plugins/parsers/snoopy SnoopyToJSON ${snoopy_filepath}/merged ${output_path}
rm ${snoopy_filepath}/merged > /dev/null 2>&1