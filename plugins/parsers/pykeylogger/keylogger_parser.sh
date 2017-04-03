#!/usr/bin/env bash
filename="$1"
output_path="$2"
clicks_dir="$3"
timed_dir="$4"

mkdir -p ${output_path}
java -cp plugins/parsers/pykeylogger KeysToJSON ${filename} ${output_path}
java -cp plugins/parsers/pykeylogger ClicksToJSON ${clicks_dir} ${output_path}
java -cp plugins/parsers/pykeylogger TimedToJSON ${timed_dir} ${output_path}
