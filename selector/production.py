
from selector.settings import *

DEBUG = False
TEMPLATE_DEBUG = False

LOGIN_URL = '/saml/admin'

try:
  from settings_local import *
except ImportError:
  pass

