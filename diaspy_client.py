import diaspy.models
import diaspy.streams
import diaspy.connection
import config

class Client:

  def __init__(self):
    self.connection = diaspy.connection.Connection(pod=config.pod, username=config.username, password=config.password)
    self.connection.login()

  def post(self, text):
    """This function sends a post to an aspect
    :param text: text to post
    :type text: str
    :returns: diaspy.models.Post -- the Post which has been created
    """
    self.stream = diaspy.streams.Stream(self.connection, 'stream.json')
    post = self.stream.post(text, aspect_ids='public', provider_display_name='foaasBot')
    return post

  def comment(self, id=0, guid='', text=''):
    """This function comments on a post
    :param post_id: ID of post to comment on
    :type post_id: int
    :param text: text of comment
    :type text: str
    """
    self.stream = diaspy.streams.Stream(self.connection, 'stream.json')
    diaspy.models.Post(self.connection, id=id, guid=guid).comment(text)

  def notifications(self):
    """Return last notifications from user"""
    n = diaspy.notifications.Notifications(self.connection)
    return n.last() # last five events

  def getPost(self, pid=0):
    """Return post by ID"""
    return diaspy.models.Post(self.connection, id=pid)

  def logout(self):
    self.connection.logout()
