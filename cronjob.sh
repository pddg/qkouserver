#!/bin/sh

BOT_MODE="qkoubot"
STREAM_MODE="stream"
DAILY_MODE="dailyjob"
USAGE_MODE="-h"
CRONTAB="/var/spool/cron/crontabs/root"
ARGS="$@"
WORK_DIR="/srv/qkouserver/"

# initialization
if [ -z ${SCRAPING_INTERVAL} ] ; then
    echo "Parameter 'SCRAPING_INTERVAL' is not given. Use default value '600'."
    SCRAPING_INTERVAL=600
fi

if [ -z ${DAILY_TWEET_HOUR} ] ; then
    echo "Parameter 'DAILY_TWEET_HOUR' is not given. Use default value '7'."
    DAILY_TWEET_HOUR=7
fi

DAILY_JOB_HOUR=${DAILY_TWEET_HOUR}
REMNANT=$((${SCRAPING_INTERVAL} % 60))
INTERVAL_MIN=`expr ${SCRAPING_INTERVAL} / 60`

showHelpMessage () {
    if `expr $1 = 1 > /dev/null` ; then
        echo "Error: Sub command not given."
    fi
    echo "Show usage for this script."
    echo "Options:"
    echo "\t-h\tshow this message."
    echo "Commands:"
    echo "\tqkoubot\t\tSetup qkoubot with cron."
    echo "\tdailyjob\tSetup qkoubot's daily job with cron."
    echo "\tstream\t\tStart streaming processing."
    exit 0
}

showArgumentError () {
    # $1 : Arguments. $@.
    echo "Error: Given argument '$1' is invalid."
    showHelpMessage 0
    exit 1
}

showVariableError () {
    # $1 : Environment variable name.
    # $2 : Messages. Something like hint.
    echo "Error: Given parameter '$1' is invalid."
    echo "$2"
    exit 1
}

startCronJob () {
    # $1 : Mode name
    # $2 : Given arguments
    # $3 : Cron parameter
    echo "======================"
    echo "MODE: $1"
    echo "======================"
    echo "Given args: \n\t$2"
    echo "Set cron job as follows."
    echo "\t""$3"
    echo "Initializing $1 ..."
    env > /env
    echo  "$3" > ${CRONTAB}
    echo "Setup was successful. Start crond."
    crond -l 2 -f
}

startStream () {
    echo "======================"
    echo "MODE: Stream"
    echo "======================"
    echo "Given args: \n\t$1"
    echo "Now starting stream processing ..."
    python3 manage.py "$@"
}

# validation
if `expr ${DAILY_TWEET_HOUR} \<= 0 > /dev/null` || `expr ${DAILY_TWEET_HOUR} \>= 24 > /dev/null` ; then
    showVariableError "DAILY_TWEET_HOUR" "It must be 0 ~ 24.\nGiven: ${DAILY_TWEET_HOUR}\nExample: 7"
fi

if `expr ${REMNANT} != 0  > /dev/null` || `expr ${SCRAPING_INTERVAL} = 0  > /dev/null`; then
    showVariableError "SCRAPING_INTERVAL" "It should be dividable by 60 and above 0.\nGiven: ${SCRAPING_INTERVAL}\nExample: 300"
fi

case "$1" in
    ${BOT_MODE})
        startCronJob "QkouBot" "${ARGS}" "*/${INTERVAL_MIN} * * * * source /env;cd ${WORK_DIR} && python3 manage.py ${ARGS}" ;;
    ${DAILY_MODE})
        startCronJob "DailyJob" "${ARGS}" "0 ${DAILY_JOB_HOUR} * * * source /env;cd ${WORK_DIR} && python3 manage.py ${ARGS}" ;;
    ${STREAM_MODE})
        startStream "$@" ;;
    ${USAGE_MODE})
        showHelpMessage 0 ;;
    *)
        if `expr $# = 0 > /dev/null` ; then
            showHelpMessage 1
        else
            showArgumentError "${ARGS}"
        fi
esac
