
import logging
import json
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView
from django.contrib.auth.decorators import login_required, permission_required
from selector.models import User
from selector.forms import SearchForm, InviteForm
from selector.roledb import paged_query

LOG = logging.getLogger(__name__)


class AdminLoginMixin(object):
  @method_decorator(login_required(login_url=reverse_lazy('login.admin')))
  @method_decorator(permission_required('selector.can_invite', login_url=reverse_lazy('permission')))
  def dispatch(self, request, *args, **kwargs):
    return super(AdminLoginMixin, self).dispatch(request, *args, **kwargs)


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
    context = {
      'form': form,
      'search_form': SearchForm(),
      'tokens': tokens,
      }
    self.template_name = self.success_template_name
    return self.render_to_response(self.get_context_data(**context))


class InvitatorView(AdminLoginMixin, TemplateView):
  template_name = 'admin.html'

  def get_context_data(self, **kwargs):
    context = super(InvitatorView, self).get_context_data(**kwargs)
    context.update({
      'meta_keys': self.request.META.keys(),
      'meta': self.request.META,
      'user': self.request.user,
    })
    return context

