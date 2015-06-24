
import logging
import json
import requests
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
  if resp.status_code not in [200, 201]:
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


