#!/bin/bash

SHOW_NAME="sunday.baroque"
DATE=$(date +"%d%b%Y")

URL="https://14073.live.streamtheworld.com/KCNVFM_SC"
# 5AM-12PM--> 7 hours in seconds
LENGTH_SECONDS=25200

OUTFILE=${HOME}/sata/incoming/${SHOW_NAME}.${DATE}.mp3

curl --output ${OUTFILE} --max-time ${LENGTH_SECONDS} --insecure  ${URL}


