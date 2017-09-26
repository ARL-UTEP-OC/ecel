#!/usr/bin/env bash

snoopyLogPath=$1
outputPath=$2

mv $1 $1.old
touch $1
tail -f $1 > $2
