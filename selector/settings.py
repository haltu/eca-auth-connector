
from django.conf import settings

ROLEDB_API_TOKEN = settings.getattr('SELECTOR_ROLEDB_API_TOKEN', '')
ROLEDB_API_ROOT = settings.getattr('SELECTOR_ROLEDB_API_ROOT', '')

# FROM DJANGO

LOGIN_REDIRECT_URL = settings.LOGIN_REDIRECT_URL

