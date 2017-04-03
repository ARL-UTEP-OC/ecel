#!/usr/bin/env bash
pcap_filepath="$1"
output_path="$2"

mergecap ${pcap_filepath}/*.*cap* -w ${pcap_filepath}/merged.pcap > /dev/null 2>&1
mkdir -p ${output_path}
java -cp plugins/parsers/tshark NetworkDataParser ${pcap_filepath}/merged.pcap ${output_path}
rm ${pcap_filepath}/merged.pcap > /dev/null 2>&1