#!/usr/bin/env bash
xmlFilePath="$1"
outputFilePath="$2"

for xmlFile in ${xmlFilePath}/*.xml; do
  outputFile=${outputFilePath}/$(echo `basename ${xmlFile}`| cut -f 1 -d '.').JSON
     if [ ! -f "$outputFile" ]
        then
                java -cp plugins/parsers/nmap/java_classes NmapDataParser ${xmlFile} $outputFile
    fi
done
