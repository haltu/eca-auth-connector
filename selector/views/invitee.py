
import logging
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.utils.encoding import force_text
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import get_current_site
from selector.models import RegisterToken
from selector.forms import RegisterForm

LOG = logging.getLogger(__name__)


class UserLoginMixin(object):
  @method_decorator(login_required(login_url=reverse_lazy('login.user')))
  def dispatch(self, request, *args, **kwargs):
    return super(UserLoginMixin, self).dispatch(request, *args, **kwargs)


class RegisterView(UserLoginMixin, FormView):
  template_name = 'register.html'
  success_url = reverse_lazy('register.success')
  failed_url = reverse_lazy('register.failed')
  form_class = RegisterForm

  def form_valid(self, form):
    token = form.cleaned_data['token']
    if token.register(self.request.user, self.request.session.get('request_meta', None)):
      return HttpResponseRedirect(self.get_success_url())
    else:
      return HttpResponseRedirect(force_text(self.failed_url))

  def get(self, request, *args, **kwargs):
    if 'token' in kwargs:
      f = RegisterForm({'token': kwargs['token']})
      if f.is_valid():
        if f.cleaned_data['token'].register(request.user, request.session.get('request_meta', None)):
          return HttpResponseRedirect(self.get_success_url())
    return super(RegisterView, self).get(request, *args, **kwargs)


class RegisterSuccessView(UserLoginMixin, TemplateView):
  template_name = 'register_success.html'


class RegisterFailedView(UserLoginMixin, TemplateView):
  template_name = 'register_failed.html'


class InviteeView(UserLoginMixin, TemplateView):
  template_name = 'user.html'

  def get_context_data(self, **kwargs):
    context = super(InviteeView, self).get_context_data(**kwargs)
    context.update({
      'meta_keys': self.request.META.keys(),
      'meta': self.request.META,
      'user': self.request.user,
    })
    return context

