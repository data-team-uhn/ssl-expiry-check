#!/bin/bash

# Runs main.py with argument values obtained from environment variables
main_py_args="--host $CHECK_HOST"

if [ ! -z $WARNING_THRESHOLD ]
then
  main_py_args="$main_py_args --warning_threshold $WARNING_THRESHOLD"
fi

if [ ! -z $SLACK_CHANNEL_URL ]
then
  main_py_args="$main_py_args --slack"
fi

python3 main.py $main_py_args
