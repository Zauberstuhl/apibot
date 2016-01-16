#!/usr/bin/env python

import re
import urllib2
import config

def foaas(command, comment=False):
  mention = "\n\n#foaas "
  m = re.search("([^@\/\s]+@[^@]+\.[^@\/\s]+)", command, re.I)
  if hasattr(m, 'group'):
    mention += "@{"+m.group(1)+" ; "+m.group(1)+"}"
    command = re.sub("([^@\/\s]+)@[^@]+\.[^@\/\s]+", r'\1', command)

  request = urllib2.Request(
    config.apiurl+urllib2.quote(command),
    headers={"Accept" : "text/plain",
    "User-Agent": "diasporaBot/1.0.0"}
  )
  contents = urllib2.urlopen(request).read()

  if comment:
    return urllib2.unquote(contents)
  else:
    return urllib2.unquote(contents) + mention
