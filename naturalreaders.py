#!/usr/bin/env python
"""
  Basic script to scrape www.naturalreaders.com for decent TTS voices
  Currently relies on a static API key so I don't know how well this will work.

"""
import argparse
import urllib
import requests


# after https://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
def download_file(url, filename):
  #local_filename = url.split('/')[-1]
  local_filename = filename
  # NOTE the stream=True parameter
  r = requests.get(url, stream=True)
  with open(local_filename, 'wb') as f:
    for chunk in r.iter_content(chunk_size=1024):
      if chunk: # filter out keep-alive new chunks
        f.write(chunk)
        #f.flush() commented by recommendation from J.F.Sebastian
  return local_filename


class Voice(object):
  def __init__(self, name, id, api):
    self._name = name
    self._id = id
    self._api = api


voices = {
  "sharon" : Voice("sharon", "42", "4"), # eng (US)
  "amanda" : Voice("amanda", "1", "4"), # eng (US)
  "tracy" : Voice("tracy", "37", "4"), # eng (US)
  "ryan" : Voice("ryan", "33", "4"), # eng (US)
  "tim" : Voice("tim", "0", "4"), # eng (US) --> El Grande Padre
  "susan" : Voice("susan", "2", "4"), # eng (US)
  "mike" : Voice("mike", "1", "0"), # eng (US) --> Moonman
  "rod" : Voice("rod", "41", "0"), # eng (US)
  "rachel" : Voice("rachel", "32", "0"), # eng (UK)
  "peter" : Voice("peter", "31", "0"),
  "graham" : Voice("graham", "25", "0"),
  "selene" : Voice("selene", "4", "4"),
  "darren" : Voice("darren", "3", "4"), # eng (UK) --> Goku
}


def do_tts(text, outfile, voice="darren", speed=""):
  global voices
  voice_data = voices[voice]
  reader = voice_data._id
  apikey="b98x9xlfs54ws4k0wc0o8g4gwc0w8ss"
  src="pw"
  text = urllib.quote(text, safe='')
 
  url = "https://api.naturalreaders.com/v4/tts/macspeak?apikey={apikey}&src={src}&r={reader}&s={speed}&t={text}".format(apikey=apikey, src=src, reader=reader, speed=speed, text=text)
  if voice_data._api == "0":
    url = "https://api.naturalreaders.com/v0/tts/?src={src}&r={reader}&s={speed}&t={text}".format(src=src, reader=reader, speed=speed, text=text) 
  download_file(url, outfile)

def main():
  parser = argparse.ArgumentParser(description='Scrape naturalreaders for TTS mp3 files.')
  parser.add_argument('text', action="store")
  parser.add_argument('-v', '--voice', type=str, default="darren")
  parser.add_argument('-s','--speed', type=str, default="-4")
  parser.add_argument('-o', '--outfile', type=str, default='output.mp3')
  args = parser.parse_args()

  print("Doing TTS for input string: '{text}'".format(text=args.text))
  print("Generating output file: {outfile}".format(outfile=args.outfile))
  
  do_tts(args.text, args.outfile, voice=args.voice, speed=args.speed)
  

if __name__ == '__main__':
  main()

