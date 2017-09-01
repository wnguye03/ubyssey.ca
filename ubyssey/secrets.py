from google.appengine.ext import ndb

class Secrets(ndb.Model):
  key = ndb.StringProperty()
  value = ndb.StringProperty()

  @staticmethod
  def get(key):
    result = Secret.query(Secret.key == key).get()
    if not result:
      raise Exception('Secret %s not found in the database' % name)
    return result.value
