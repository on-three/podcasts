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






