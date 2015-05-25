
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from selector.models import RegisterToken


class Command(BaseCommand):
  def handle(self, *args, **options):
    dt = datetime.now() - timedelta(seconds=settings.TOKEN_EXPIRE)
    for t in RegisterToken.objects.filter(sent=False, issued_at=dt):
      print 'False', repr(t.user.pk), t.method, t.token
      t.delete()
    for t in RegisterToken.objects.filter(sent=True):
      print 'True', repr(t.user.pk), t.method, t.token
      t.delete()


