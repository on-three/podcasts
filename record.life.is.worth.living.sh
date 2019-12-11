#!/bin/bash

# record an m3u8 stream for N seconds
STREAM="https://d3je5q1nueb5wn.cloudfront.net/p/DOME_1920x1080_4000k.m3u8"
SHOW_NAME=Life.Is.Worth.Living
DATE=DATE=$(date +"%d%b%Y")

LENGTH_SECONDS=1800

OUTFILE=${HOME}/sata/incoming/${SHOW_NAME}.${DATE}.mp4

ffmpeg -i "${STREAM}" -c copy -bsf:a aac_adtstoasc -t ${LENGTH_SECONDS} ${OUTFILE}