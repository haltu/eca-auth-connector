# -*- encoding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2015 Haltu Oy, http://haltu.fi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import logging
import json
import requests
from selector import settings

LOG = logging.getLogger(__name__)


class APIResponse(Exception):
  def __init__(self, resp):
    self.r = resp

  def __str__(self):
    u = super(APIResponse, self).__str__()
    return u + '\nResponse: %s' % self.r


def make_request(method, url, **kwargs):
  kwargs['headers'] = {
    'Authorization': 'Token %s' % settings.ROLEDB_API_TOKEN,
    'Content-Type': 'application/json',
  }
  kwargs['verify'] = False  # Disabled SSL certificate checks
  method = getattr(requests, method)
  try:
    resp = method(url, **kwargs)
  except requests.exceptions.RequestException:
    LOG.exception('Auth Data API call failed')
    raise APIResponse('Auth Data API call failed')
  if resp.status_code not in [200, 201, 204]:
    raise APIResponse(resp)
  if resp.status_code == 204:
    return {}
  content = resp.content
  return json.loads(content)


def roledb_client(method, api, **kwargs):
  url = settings.ROLEDB_API_ROOT + api
  if '?' not in url and not url.endswith('/'):
    url = url + '/'
  if 'data' in kwargs:
    kwargs['data'] = json.dumps(kwargs['data'])
  print repr(url), repr(kwargs)
  return make_request(method, url, **kwargs)


def paged_query(*args, **kwargs):
  """ Compiles paginated query to the API.
  Fetches All objects.
  """
  r = roledb_client(*args, **kwargs)
  for o in r['results']:
    yield o
  if 'next' in r:
    while r['next']:
      r = make_request('get', r['next'])
      for o in r['results']:
        yield o

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

