#!/bin/bash
#Script for recording temperature

FILE=${1:-~/logs/temp_history.log}

while true
do

	TEMP=$(/opt/vc/bin/vcgencmd measure_temp | grep -o '[0-9.]\+')
	DATE=$(date +"%Y-%m-%d %T")
	ROW="$DATE $TEMP"

	echo $ROW
	echo $ROW  >> $FILE

	sleep 1
done
