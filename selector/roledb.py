
import logging
import json
from django.http import Http404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django import forms
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_text
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import TemplateView, FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.sites.models import get_current_site
import requests
from selector.models import User, RegisterToken
from selector.forms import SearchForm, InviteForm, RegisterForm
from selector import settings

LOG = logging.getLogger(__name__)

class APIResponse(Exception):
  def __init__(self, resp):
    self.r = resp

def roledb_client(method, api, **kwargs):
  kwargs['headers'] = {
    'Authorization': 'Token %s' % settings.ROLEDB_API_TOKEN,
    'Content-Type': 'application/json',
    }
  kwargs['verify'] = False # Disabled SSL certificate checks
  url = settings.ROLEDB_API_ROOT + api
  if not '?' in url and not url.endswith('/'):
    url = url + '/'
  if 'data' in kwargs:
    kwargs['data'] = json.dumps(kwargs['data'])
  print repr(url), repr(kwargs)
  method = getattr(requests, method)
  resp = method(url, **kwargs)
  if resp.status_code != 200:
    raise APIResponse(resp)
  content = resp.content
  return json.loads(content)


def paged_query(*args, **kwargs):
  """ Compiles paginated query to the API.
  Fetches All objects.
  """
  r = roledb_client(*args, **kwargs)
  for o in r['results']:
    yield o
  if 'next' in r:
    while r['next']:
      r = client('get', r['next'])
      for o in r['results']:
        yield o


