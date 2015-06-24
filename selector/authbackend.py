import logging
from django.contrib.auth.backends import ModelBackend
from selector.models import User

LOG = logging.getLogger(__name__)


class ShibbolethBackend(ModelBackend):
  def authenticate(self, **credentials):
    if not 'request_meta' in credentials:
      return None
    if not 'HTTP_USER_OID' in credentials['request_meta']:
      LOG.debug('no HTTP_USER_OID in request.META')
      return None
    uid = credentials['request_meta']['HTTP_USER_OID']
    LOG.debug('ShibbolethBackend.authenticate',
        extra={'data': {'uid': uid}})
    try:
      # TODO Check also the organisation
      user = User.objects.get(username=uid)
    except User.DoesNotExist:
      return None
    return user

