
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


class AdminLoginMixin(object):
  @method_decorator(login_required(login_url=reverse_lazy('login.admin')))
  def dispatch(self, request, *args, **kwargs):
    return super(AdminLoginMixin, self).dispatch(request, *args, **kwargs)


class UserLoginMixin(object):
  @method_decorator(login_required(login_url=reverse_lazy('login.user')))
  def dispatch(self, request, *args, **kwargs):
    return super(UserLoginMixin, self).dispatch(request, *args, **kwargs)


class IndexView(TemplateView):
  template_name = 'index.html'

  def get_context_data(self, **kwargs):
    context = super(TemplateView, self).get_context_data(**kwargs)
    context.update({
      'meta_keys': self.request.META.keys(),
      'meta': self.request.META,
      'user': self.request.user,
    })
    return context


class SearchView(AdminLoginMixin, FormView):
  template_name = 'search.html'
  form_class = SearchForm

  def form_valid(self, form):
    users = []
    for d in paged_query('get', 'user', params=form.cleaned_data):
      users.append((d['username'], d['username']))
    self.request.session['inviteform_users_choices'] = users
    # TODO: Or we could just send the user to InviteView here
    invite_form = InviteForm(users_choices=users)
    context = {
      'form': form,
      'invite_form': invite_form,
      'data': json.dumps(users), # for debug
      }
    return self.render_to_response(self.get_context_data(**context))


class InviteView(AdminLoginMixin, FormView):
  template_name = 'invite.html'
  success_template_name = 'invited.html'
  form_class = InviteForm

  def get_form_kwargs(self):
    kwargs = super(InviteView, self).get_form_kwargs()
    kwargs['users_choices'] = self.request.session.get('inviteform_users_choices')
    return kwargs

  def form_valid(self, form):
    tokens = []
    for u in form.cleaned_data['users']:
      user,_ = User.objects.get_or_create(username=u)
      ts = user.create_register_tokens()
      tokens.append(*ts)
      print repr(ts)
    context = {
      'form': form,
      'search_form': SearchForm(),
      'tokens': tokens,
      }
    self.template_name = self.success_template_name
    return self.render_to_response(self.get_context_data(**context))


class RegisterView(UserLoginMixin, FormView):
  template_name = 'register.html'
  success_url = reverse_lazy('register.success')
  failed_url = reverse_lazy('register.failed')
  form_class = RegisterForm

  def form_valid(self, form):
    token = RegisterToken.objects.get(token=form.cleaned_data['token'], method=RegisterToken.EMAIL)
    if token.register(self.request.user, self.request.session.get('request_meta', None)):
      return HttpResponseRedirect(self.get_success_url())
    else:
      return HttpResponseRedirect(force_text(self.failed_url))

  def get(self, request, *args, **kwargs):
    if 'token' in kwargs:
      try:
        token = RegisterToken.objects.get(token=kwargs.get('token'), method=RegisterToken.EMAIL)
        if token.register(request.user, request.session.get('request_meta', None)):
          return HttpResponseRedirect(self.get_success_url())
      except RegisterToken.DoesNotExist:
        pass
    return super(RegisterView, self).get(request, *args, **kwargs)


class RegisterSuccessView(UserLoginMixin, TemplateView):
  template_name = 'register_success.html'


class RegisterFailedView(UserLoginMixin, TemplateView):
  template_name = 'register_failed.html'


class InvitatorView(AdminLoginMixin, TemplateView):
  template_name = 'admin.html'

  def get_context_data(self, **kwargs):
    context = super(TemplateView, self).get_context_data(**kwargs)
    context.update({
      'meta_keys': self.request.META.keys(),
      'meta': self.request.META,
      'user': self.request.user,
    })
    return context


class InviteeView(UserLoginMixin, TemplateView):
  template_name = 'user.html'


@sensitive_post_parameters()
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          current_app=None, extra_context=None):
    """
    Does the login by passing request.META to authbackend.
    If no identity found then shows the template.
    """
    redirect_to_request = request.REQUEST.get(redirect_field_name, '')
    redirect_to = settings.LOGIN_REDIRECT_URL

    # Ensure the user-originating redirection url is safe.
    if is_safe_url(url=redirect_to_request, host=request.get_host()):
        redirect_to = redirect_to_request
    else:
        redirect_to = settings.LOGIN_REDIRECT_URL

    user = authenticate(request_meta=request.META)
    if not user:
        LOG.info('Could not authenticate user from the headers')
    if user:
        # Okay, security check complete. Log the user in.
        auth_login(request, user)
        meta = {}
        for k in ['HTTP_USER_IDENTITY',]:
          meta[k] = request.META[k]
        request.session['request_meta'] = meta
        return HttpResponseRedirect(redirect_to)

    current_site = get_current_site(request)
    context = {
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
        'meta': request.META,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context, current_app=current_app)

