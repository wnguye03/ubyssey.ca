from google.appengine.ext import vendor

# Patch to fix GCS in django-storages
import tempfile
tempfile.SpooledTemporaryFile = tempfile.TemporaryFile

# Add any libraries installed in the "lib" folder.
vendor.add('lib')
