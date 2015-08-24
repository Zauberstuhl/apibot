#! /usr/bin/env python

from time import gmtime, strftime
from foaas import foaas
from diaspy_client import Client

import re
import urllib2

def log_write(text):
  f = open('bot.log', 'a')
  f.write(strftime("%a, %d %b %Y %H:%M:%S ", gmtime()))
  f.write(text)
  f.write('\n')
  f.close()

client=Client()
notify = client.notifications()
for n in notify:
  if not n.unread: continue
  m = re.search('\shas\smentioned.+post\s([^\/]+)\s(.+)\.+$', str(n))
  try:
    if hasattr(m, 'group'):
      command = m.group(2).replace(' ', '__')
      client.post(foaas(command))

    # finally mark as read
    n.mark()
  except urllib2.URLError:
    log_write("ERROR: "+str(n))
