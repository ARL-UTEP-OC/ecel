#!/usr/bin/env bash
clicks_dir="$1"
output_path="$2"

mkdir -p ${output_path}
java -cp plugins/parsers/manualscreenshot ManualScreenshotToJSON ${clicks_dir} ${output_path}