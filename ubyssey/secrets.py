# import ndb_orm as ndb
# from google.cloud import datastore

# client = datastore.Client()
# ndb.enable_use_with_gcd(client.project)

# class Secrets(ndb.Model):
#     key = ndb.TextProperty(indexed=False)
#     value = ndb.TextProperty(indexed=False)

#     @staticmethod
#     def get(key):
#         PLACEHOLDER_VALUE = 'NOT SET'

#         result = Secrets.query(Secrets.key == key).get()

#         if not result:
#             result = Secrets()
#             result.key = key
#             result.value = PLACEHOLDER_VALUE
#             result.put()

#         if result.value == PLACEHOLDER_VALUE:
#             raise Exception('Secret %s not defined in the Secrets database.' % key)

#         return result.value
