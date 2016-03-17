import os

os.environ.setdefault("DISPATCH_PROJECT_DIR", os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("DISPATCH_PROJECT_MODULE", "ubyssey")

from dispatch.core.wsgi import get_wsgi_application

application = get_wsgi_application()
