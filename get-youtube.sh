#!/bin/bash

URL="$1"
OUTFILE="$2"
TMPFILE=/tmp/tmpyoutubedl.file.mp3
SAMPLERATE=44100
EXT=mp3

# download arg 1, audio only to mp3, forcing filename
youtube-dl --no-mtime --extract-audio --audio-format ${EXT} --output $TMPFILE "$1"

# force sample rate that is supported for my xdoo shit device
ffmpeg -i $TMPFILE -ar $SAMPLERATE ${OUTFILE}.${EXT}

