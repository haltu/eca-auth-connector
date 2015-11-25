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
#

import logging
from django.contrib.auth.backends import ModelBackend
from selector.models import User

LOG = logging.getLogger(__name__)


class ShibbolethBackend(ModelBackend):
  def authenticate(self, **credentials):
    if not 'request_meta' in credentials:
      return None
    if not 'HTTP_MPASS_OID' in credentials['request_meta']:
      LOG.debug('no HTTP_MPASS_OID in request.META')
      return None
    uid = credentials['request_meta']['HTTP_MPASS_OID']
    LOG.debug('ShibbolethBackend.authenticate',
        extra={'data': {'uid': uid}})
    try:
      # TODO Check also the organisation
      user = User.objects.get(username=uid)
    except User.DoesNotExist:
      return None
    return user

