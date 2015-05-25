
from django.conf import settings

ROLEDB_API_TOKEN = getattr(settings, 'SELECTOR_ROLEDB_API_TOKEN', '')
ROLEDB_API_ROOT = getattr(settings, 'SELECTOR_ROLEDB_API_ROOT', '')
TOKEN_EXPIRE = getattr(settings, 'SELECTOR_TOKEN_EXPIRE', 3*24*60*60)


# FROM DJANGO

LOGIN_REDIRECT_URL = settings.LOGIN_REDIRECT_URL

