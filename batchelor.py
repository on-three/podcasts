#!/usr/bin/env python
"""
FILE: batchelor.py
DESC: put John Batchelor podcast episodes back together

"""
import argparse
import os.path
import re
import feedparser
from naturalreaders import do_tts

SHOW_NAME='the.John.Batchelor.Show'


def download_segment(name, url, title, trim=False, intro=True, force=False):
  # does the file already exist? if so don't download again
  if os.path.exists(name):
    return True

  call = 'wget --tries=5 --user-agent="Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0" -O "{name}" "{url}"'.format(name=name, url=url)
  os.system(call)

  if not os.path.exists(name):
    return False

  if trim:
    raw_name = name + '.raw.mp3'
    raw_cmd = 'mv {n} {r}'.format(n=name, r=raw_name)
    os.system(raw_cmd)
    c = 'ffmpeg -i {raw_name} -y -ss {t} -vcodec copy -acodec copy {name}'.format(t=60, raw_name=raw_name, name=name)
    print("*****" + c + "*******")
    os.system(c)

  if intro:
    raw_name = name + '.raw.mp3'
    raw_cmd = 'mv {n} {r}'.format(n=name, r=raw_name)
    os.system(raw_cmd)
    desc_file = name + '.desc.mp3'
    if not os.path.exists(desc_file):
      do_tts(title, desc_file, voice='tim')

    # concat the desc to the front of the raw file
    #ffmpeg -i 'concat:input1|input2' -codec copy output
    concat_cmd = 'ffmpeg -i \'concat:{f1}|{f2}\' -codec copy {name}'.format(f1=desc_file, f2=raw_name, name=name)
    os.system(concat_cmd)

  return True


def aggregate_files(outfile, tmp_files, force=False):
  global SHOW_NAME
  print "aggregating files into " + outfile
  ## this is a comment
  #file '/path/to/file1'
  #file '/path/to/file2'
  #file '/path/to/file3'
  listfile = '/tmp/concatenate.txt'
  f = open(listfile, 'w+')
  for l in tmp_files:
    f.write('file {filename}\n'.format(filename=l))
  f.close()

  call = 'ffmpeg -y -f concat -safe 0 -i {f} -c copy {outfile}'.format(f=listfile, outfile=outfile)
  os.system(call)

def reassemble_program(rss, trim=False, out_dir='.', tmp_dir='/tmp'):
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

  if len(newest_entries) < 1:
    print("**** couldn't find any entries in rss feed.")
    return

  files = []
  for entry in sorted_entries:
    date = entry['published_parsed']
    #tm_year=2018, tm_mon=2, tm_mday=17
    if date.tm_year != today.tm_year or date.tm_mon != today.tm_mon or date.tm_mday != today.tm_mday:
      continue;
  
    files.append(entry)
    
  i = 0
  tmp_files = []
  basename = SHOW_NAME + '.' + str(today.tm_mon) + '.' + str(today.tm_mday) + '.' + str(today.tm_year)
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
    download_segment(tmp_file, mp3, title, trim=trim)
    tmp_files.append(tmp_file)

  outfile = out_dir + '/' + basename + '.mp3' 

  aggregate_files(outfile, tmp_files)


  print 'Aggregation complete'

"""
"""

def main():
  parser = argparse.ArgumentParser(description='Reassemble John Batchelor episode from RSS feed.')
  parser.add_argument('--rss', action="store", default="https://audioboom.com/channels/4002274.rss")
  parser.add_argument('-t', '--trim', action="store_true", default=True, help='trim one minute from front end of all segments.')
  #parser.add_argument('--phonemes', action="store_true", default=False)
  #parser.add_argument('--videos', action="store_true", default=False)
  parser.add_argument('-o', '--outdir', type=str, default='./tmp/')
  args = parser.parse_args()

  #print(" in dir: {dir}".format(dir=args.outdir))

  rss = args.rss
  trim = args.trim

  #infile = args.infile
  #if not os.path.isfile(infile):
  #  print("File: " + infile + " not found.")
  #  return -1

  reassemble_program(rss, trim=trim)



if __name__ == '__main__':
  main()






