#!/bin/bash

#send stdout and stderr to a log file
exec 3>&1 4>&2 1>> ${LOG_DIR}/log_api 2>&1

# activate virtual environment
echo "activate the python virtual environment"
. ${VIRTUAL_ENV}/bin/activate

#print date with hours minutes and seconds in the log file
echo "$(date '+%Y-%m-%d %H:%M:%S') Starting ml api"

cd ${PY_APP_DIR}/covid_py_ml

# reminder api = api.py, app is always on the right of the colon
gunicorn --bind 0.0.0.0:8080 api:app -D


#Add a space at the end of this section in the log file
printf "\n"
printf "\n"


# stop logging and print complete to the terminal
exec 1>&3 2>&4
echo >&2 "complete"
