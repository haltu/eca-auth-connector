
from django.conf import settings

ROLEDB_API_TOKEN = settings.getattr('SELECTOR_ROLEDB_API_TOKEN', '')
ROLEDB_API_ROOT = settings.getattr('SELECTOR_ROLEDB_API_ROOT', '')
TOKEN_EXPIRE = settings.getattr('SELECTOR_TOKEN_EXPIRE', 3*24*60*60)


# FROM DJANGO

LOGIN_REDIRECT_URL = settings.LOGIN_REDIRECT_URL

