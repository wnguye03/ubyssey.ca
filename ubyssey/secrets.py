from google.appengine.ext import ndb

class Secrets(ndb.Model):
  key = ndb.StringProperty()
  value = ndb.StringProperty()

  @staticmethod
  def get(key):
    PLACEHOLDER_VALUE = 'NOT SET'

    result = Secret.query(Secret.key == key).get()

    if not result:
        result = Secrets()
        result.name = name
        result.value = PLACEHOLDER_VALUE
        result.put()

    if result.value == PLACEHOLDER_VALUE:
        raise Exception('Secret %s not defined in the Secrets database.' % key)

    return result.value
