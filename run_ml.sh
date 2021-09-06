#!/bin/bash

#send stdout and stderr to a log file
exec 3>&1 4>&2 1>> ${LOG_DIR}/log_ml 2>&1

# activate virtual environment
echo "activate the python virtual environment"
. ${VIRTUAL_ENV}/bin/activate

while true
do
        #print date with hours minutes and seconds in the log file
        echo "$(date '+%Y-%m-%d %H:%M:%S') Starting machine learning routine"

        python3 ${PY_APP_DIR}/covid_py_ml/ml.py

		
        #Add a space at the end of this section in the log file
        printf "\n"


	# determine how many seconds to sleep so that the next routine runs at 15 min past the hour every one hour

	# current epoch in seconds
	now_seconds=$(date +'%s')

	# determine target date and time with hour, but no minutes
	target_date_hour=$(date -d "now + 1 hour" +'%m/%d/%Y %H')

	# determine the epoch in seconds for the next target time
	target_seconds=$(date -d "$target_date_hour:15" +'%s')

	# calculate the number of seconds between now the target time
	sleep_seconds=$(( $target_seconds - $now_seconds ))

	echo "sleeping for $sleep_seconds"
	sleep $sleep_seconds

     #Add a space at the end of this section in the log file
    printf "\n"
    printf "\n"

done

# stop logging and print complete to the terminal
exec 1>&3 2>&4
echo >&2 "complete"
