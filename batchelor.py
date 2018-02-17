#!/usr/bin/env python
"""
FILE: batchelor.py
DESC: put John Batchelor podcast episodes back together

"""
import argparse
import os.path
import re
import feedparser

def reassemble_program(rss):
  """
  """
  print 'Aggregating episode at rss: ' + rss
  feed = feedparser.parse( rss )
  print feed[ "channel" ][ "title" ]
  print feed[ "channel" ][ "description" ]

  #print feed[ 'channel' ]['item'][ 'media_content']

  #print str(feed)

  # sort channel entries, most recent first
  entries = feed['entries']
  sorted_entries = sorted(entries, key=lambda entry: entry["published_parsed"])
  newest_entries = sorted(entries, key=lambda entry: entry["published_parsed"])
  newest_entries.reverse() # for most recent entries first

  #only take entries from the latest episode
  today = newest_entries[0]['published_parsed']
  print 'Aggregating segments for show from ' + str(today)

  i = 0
  for entry in sorted_entries:
    date = entry['published_parsed']
    #tm_year=2018, tm_mon=2, tm_mday=17
    if date.tm_year != today.tm_year or date.tm_mon != today.tm_mon or date.tm_mday != today.tm_mday:
      continue;
  
    print str(i) + '+++++++++++'
    title = entry['title']
    print title
    
    print str(date)
    mp3 = entry['media_content'][0]['url']
    #img = entry['media_content'][1]['url']
    print 'mp3 ' + mp3
    print '++++++++++++'
    i = i + 1

  print 'Aggregation complete'

"""
"""

def main():
  parser = argparse.ArgumentParser(description='Reassemble John Batchelor episode from RSS feed.')
  parser.add_argument('--rss', action="store", default="https://audioboom.com/channels/4002274.rss")
  #parser.add_argument('--tts', action="store_true", default=False)
  #parser.add_argument('--phonemes', action="store_true", default=False)
  #parser.add_argument('--videos', action="store_true", default=False)
  parser.add_argument('-o', '--outdir', type=str, default='./tmp/')
  args = parser.parse_args()

  #print(" in dir: {dir}".format(dir=args.outdir))

  rss = args.rss

  #infile = args.infile
  #if not os.path.isfile(infile):
  #  print("File: " + infile + " not found.")
  #  return -1

  reassemble_program(rss)



if __name__ == '__main__':
  main()






