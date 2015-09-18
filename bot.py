#! /usr/bin/env python

from time import gmtime, strftime
from foaas import foaas
from diaspy_client import Client

import config
import re
import urllib2

client = Client()
notify = client.notifications()
for n in notify:
  if not n.unread: continue
  idm = re.search('href=\\"/posts/(\d+?)\\"', n._data['note_html'])

  if (n.type == "mentioned" and hasattr(idm, 'group')):
    post_id = idm.group(1)
    post = client.getPost(post_id)
    text = post._data['text']
    m = re.search('^\s*\@\{[^\};]+;[^\};]+\}\s+(\/.+?)$', text)
    if hasattr(m, 'group'):
      try:
        command = m.group(1)
        client.post(foaas(command))
      except urllib2.URLError:
        client.comment(post_id, "Fuck this! Something went wrong :\\")
    else:
      comment_exist = False
      for comment in post.comments:
        if comment._data['author']['guid'] == config.profile_guid:
          comment_exist = True
      if not comment_exist:
        client.comment(post_id,
          "Fuck this! Your command is not well-formed.\n"
          "Check my [profile description](/people/448c48d02c1c013349f314dae9b624ce) or "
          "[fuck around with him...](/posts/0f99d95040130133bbca14dae9b624ce)")

  # mark as read if it
  # is not a mention
  n.mark()

client.logout()
