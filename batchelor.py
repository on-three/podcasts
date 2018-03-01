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
from mutagen.mp3 import MP3

SHOW_NAME='the.John.Batchelor.Show'

class SimpleDate(object):
  def __init__(self, date_string):
    d = date_string.split(':')
    self.tm_mon = int(d[0])
    self.tm_mday = int(d[1])
    self.tm_year = int(d[2])
    
def get_runnning_time_seconds(filename):
  audio = MP3(filename)
  return int(audio.info.length)


def download_segment(name, url, title, trim=43, intro=True, force=False):
  # does the file already exist? if so don't download again
  if os.path.exists(name) and not force:
    return True

  print("File " + name + " does not exist.")
  print("Downloading sement of show at url: " + url)

  call = 'wget --tries=5 --user-agent="Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0" -O "{name}" "{url}"'.format(name=name, url=url)
  print "****" + call + "****"
  os.system(call)

  if not os.path.exists(name):
    return False

  if trim > 0:
    COMMERCIAL_LENGTH = trim
    # we want to trim a second from the start and end of the file
    # but to do that ffmpeg needs the entire running time (piece of shit)
    length_s = get_runnning_time_seconds(name)
    print("Length of file {f} found to be {s}".format(f=name, s=length_s))
    trimmed_length = length_s - COMMERCIAL_LENGTH * 2 

    raw_name = name + '.raw.mp3'
    raw_cmd = 'mv {n} {r}'.format(n=name, r=raw_name)
    os.system(raw_cmd)
    
    c = 'ffmpeg -i {raw_name} -y -ss {t} -t {l} -vcodec copy -acodec copy {name}'.format(t=COMMERCIAL_LENGTH, l=trimmed_length, raw_name=raw_name, name=name)
    print "+++++++" + c + "+++++++"
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

def reassemble_program(rss, trim=43, force=False, out_dir='./', tmp_dir='/tmp', date=None):
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

  #only take entries from the latest episode if no date provided
  today = newest_entries[0]['published_parsed']
  if date:
    today = SimpleDate(date)
  print 'Aggregating segments for show from ' + str(today.tm_mon) + ':' + str(today.tm_mday) + ':' + str(today.tm_year)

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
    _date = entry['published_parsed']
    #tm_year=2018, tm_mon=2, tm_mday=17
    if _date.tm_year != today.tm_year or _date.tm_mon != today.tm_mon or _date.tm_mday != today.tm_mday:
      continue;
  
    files.append(entry)

  if len(files) == 0:
    print("Could not find any rss entries for indicated date. Bailing.")
    return
    
  i = 0
  tmp_files = []
  for f in files:
    # we want to do simple English TTS on titles, so make them simle ascii
    title = f['title'].encode('ascii', errors='ignore')
    mp3 = f['media_content'][0]['url']
    #img = entry['media_content'][1]['url']
    i = i + 1

    # download the segment
    tmp_file = tmp_dir + '/' + basename + '.' + str(i) + '.mp3'
    if not download_segment(tmp_file, mp3, title, trim=trim, force=force):
      print("Downloading segment " + tmp_file + " at url: " + mp3 + " failed for some reason. Bailing.")
      return False
    tmp_files.append(tmp_file)


  aggregate_files(outfile, tmp_files)


  print 'Aggregation complete'

"""
"""

def main():
  parser = argparse.ArgumentParser(description='Reassemble John Batchelor episode from RSS feed.')
  parser.add_argument('--rss', action="store", default="https://audioboom.com/channels/4002274.rss")
  parser.add_argument('-t', '--trim', type=int, default=43, help='trim n seconds from the front end back of each segment.')
  parser.add_argument('--force', action="store_true", default=False, help='Force redownload and reconstruction of entire file.')
  parser.add_argument('-o', '--outdir', type=str, default='./', help='Directory to put final reconstructed file.')
  parser.add_argument('--tmpdir', type=str, default='/tmp', help='Directory used for temporary work files.')
  parser.add_argument('--date', type=str, default=None, help='Reconstruct a show on a specific date in the form "month:day:fullyear" e.g. "2:17:2018"')
  args = parser.parse_args()


  rss = args.rss
  trim = args.trim
  force = args.force
  out_dir = args.outdir
  tmp_dir = args.tmpdir
  date = args.date
  if date:
    # check our date is of the correct form
    date_regex = r'[0-9]{1,2}:[0-9]{1,2}:[0-9]{4}'
    if not re.match(date_regex, date):
      print 'Provided date argument ' + date + ' is not correct. Use form "2:21:2018"'
      return
    else:
      print 'Will attempt to reconstruct show for date: ' + date

  reassemble_program(rss, out_dir=out_dir, tmp_dir=tmp_dir, trim=trim, force=force, date=date)



if __name__ == '__main__':
  main()






