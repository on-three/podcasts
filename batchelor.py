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
  if os.path.exists(name) and not force:
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

def reassemble_program(rss, trim=False, force=False, out_dir='.', tmp_dir='/tmp'):
  """
  """
  print 'Aggregating episode at rss: ' + rss
  feed = feedparser.parse( rss )
  print feed[ "channel" ][ "title" ]
  print feed[ "channel" ][ "description" ]
  
  # DEBUG
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
    return False

  # don't regenerate the target file unless forced
  basename = SHOW_NAME + '.' + str(today.tm_mon) + '.' + str(today.tm_mday) + '.' + str(today.tm_year)
  outfile = out_dir + '/' + basename + '.mp3'
  if os.path.exists(outfile) and not force:
    print "Target file: " + outfile + " already exists. Use --force to reconstruct."
    return False
 
  files = []
  for entry in sorted_entries:
    date = entry['published_parsed']
    #tm_year=2018, tm_mon=2, tm_mday=17
    if date.tm_year != today.tm_year or date.tm_mon != today.tm_mon or date.tm_mday != today.tm_mday:
      continue;
  
    files.append(entry)
    
  i = 0
  tmp_files = []
  for f in files:
    date = f['published_parsed']
    title = f['title']
    mp3 = f['media_content'][0]['url']
    #img = entry['media_content'][1]['url']
    i = i + 1

    # download the segment
    tmp_file = tmp_dir + '/' + basename + '.' + str(i) + '.mp3'
    download_segment(tmp_file, mp3, title, trim=trim, force=force)
    tmp_files.append(tmp_file)


  aggregate_files(outfile, tmp_files)


  print 'Aggregation complete'

"""
"""

def main():
  parser = argparse.ArgumentParser(description='Reassemble John Batchelor episode from RSS feed.')
  parser.add_argument('--rss', action="store", default="https://audioboom.com/channels/4002274.rss")
  parser.add_argument('-t', '--trim', action="store_true", default=True, help='trim one minute from front end of all segments.')
  parser.add_argument('--force', action="store_true", default=False, help='Force redownload and reconstruction of entire file.')
  parser.add_argument('-o', '--outdir', type=str, default='./tmp/')
  args = parser.parse_args()


  rss = args.rss
  trim = args.trim
  force = args.force

  reassemble_program(rss, trim=trim, force=force)



if __name__ == '__main__':
  main()






