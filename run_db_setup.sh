#!/bin/bash

#send stdout and stderr to a log file
exec 3>&1 4>&2 1>> ${LOG_DIR}/log_setup_db 2>&1

# activate virtual environment
echo "activate the python virtual environment"
. ${VIRTUAL_ENV}/bin/activate

#print date with hours minutes and seconds in the log file
echo "$(date '+%Y-%m-%d %H:%M:%S') starting db setup"

python3 ${PY_APP_DIR}/covid_py_ml/db_setup.py

#Add a space at the end of this section in the log file
printf "\n"
printf "\n"


# stop logging and print complete to the terminal
exec 1>&3 2>&4
echo >&2 "complete"
