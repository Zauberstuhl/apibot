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
  idm = re.search('href=\\"/posts/(\d+?)\\"', n._data['note_html'])

  if hasattr(idm, 'group'):
    text = client.getPostText(idm.group(1))
    m = re.search('^\s*\@\{[^\};]+;[^\};]+\}\s+(\/.+?)$', text)
    if hasattr(m, 'group'):
      try:
        command = m.group(1)
        client.post(foaas(command))
      except urllib2.URLError:
        log_write("ERROR: "+command)

  # mark as read if it
  # is not a mention
  n.mark()

client.logout()
