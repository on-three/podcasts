#!/usr/bin/env python
"""
FILE: batchelor.py
DESC: put John Batchelor podcast episodes back together

"""
import argparse
import os.path
import re
import feedparser


def download_segment(name, url, force=False):
  #does the file already exist? if so don't download again
  if os.path.exists(name):
    return True
  call = 'wget -O "{name}" "{url}"'.format(name=name, url=url)
  os.system(call)

  if not os.path.exists(name):
    return False

  return True


def aggregate_files(outfile, tmp_files, force=False):
  print "aggregating files into " + outfile

def reassemble_program(rss, out_dir='.', tmp_dir='/tmp'):
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

  files = []
  for entry in sorted_entries:
    date = entry['published_parsed']
    #tm_year=2018, tm_mon=2, tm_mday=17
    if date.tm_year != today.tm_year or date.tm_mon != today.tm_mon or date.tm_mday != today.tm_mday:
      continue;
  
    files.append(entry)
    
  i = 0
  tmp_files = []
  basename = 'bachelor.' + str(today.tm_mon) + '.' + str(today.tm_mday) + '.' + str(today.tm_year)
  for f in files:
    date = f['published_parsed']
    print str(i) + '+++++++++++'
    title = f['title']
    print title
    
    print str(date)
    mp3 = f['media_content'][0]['url']
    #img = entry['media_content'][1]['url']
    print 'mp3 ' + mp3
    print '++++++++++++'
    i = i + 1

    # download the segment
    tmp_file = tmp_dir + '/' + basename + '.' + str(i) + '.mp3'
    download_segment(tmp_file, mp3)
    tmp_files.append(tmp_file)

  outfile = out_dir + '/' + basename + '.mp3' 

  aggregate_files(outfile, tmp_files)


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






