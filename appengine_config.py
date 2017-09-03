from google.appengine.ext import vendor

# import tempfile
#
# # Patch to fix GCS in django-storages
# class CustomSpooledTemporaryFile(tempfile.TemporaryFile):
#     def __init__(max_size=0, mode='w+b', bufsize=-1, suffix='', prefix='tmp', dir=None):
#         super(SpooledTemporaryFile, self).__init__(mode, bufsize, suffix, prefix, dir)
#
# tempfile.SpooledTemporaryFile = CustomSpooledTemporaryFile

# Add any libraries installed in the "lib" folder.
vendor.add('lib')
