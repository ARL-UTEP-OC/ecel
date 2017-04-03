#!/usr/bin/env bash

snoopyLogPath=$1
outputPath=$2

tail -f $1 > $2