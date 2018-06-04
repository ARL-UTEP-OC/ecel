#!/usr/bin/env bash
pcap_filepath="$1"
output_path="$2"
model_path="$3"

mergecap ${pcap_filepath}/*.*cap* -w ${pcap_filepath}/merged.pcap > /dev/null 2>&1
mkdir -p ${output_path}
java -cp plugins/parsers/tshark NetworkDataParser ${pcap_filepath}/merged.pcap ${output_path}
${model_path}run.sh -c 250 -i ${pcap_filepath}/merged.pcap -d ${model_path} -o ${output_path}'/networkDataModel.JSON'
rm ${pcap_filepath}/merged.pcap > /dev/null 2>&1
