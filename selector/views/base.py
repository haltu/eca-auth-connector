
import logging
from django.views.generic import TemplateView

LOG = logging.getLogger(__name__)


class IndexView(TemplateView):
  template_name = 'index.html'

  def get_context_data(self, **kwargs):
    context = super(IndexView, self).get_context_data(**kwargs)
    context.update({
      'meta_keys': self.request.META.keys(),
      'meta': self.request.META,
      'user': self.request.user,
    })
    return context

class PermissionView(TemplateView):
  template_name = 'permission.html'


