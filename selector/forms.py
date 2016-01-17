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


import floppyforms as forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.text import capfirst
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from selector.models import User, RegisterToken


class UserSelectWidget(forms.CheckboxSelectMultiple):
  template_name = 'forms/inviteform_user.html'


class SearchForm(forms.Form):
  municipality = forms.CharField()
  school = forms.CharField()
  group = forms.CharField(required=False)


class InviteForm(forms.Form):
  users = forms.MultipleChoiceField(choices=set(), widget=UserSelectWidget)

  def __init__(self, *args, **kwargs):
    if 'users_choices' in kwargs:
      users_choices = kwargs.pop('users_choices')
    else:
      users_choices = set()
    if users_choices == None:
      users_choices = set()
    super(InviteForm, self).__init__(*args, **kwargs)
    self.fields['users'].choices = users_choices


class RegisterForm(forms.Form):
  token = forms.CharField()

  def clean_token(self):
    try:
      token = RegisterToken.objects.get(token=self.cleaned_data['token'], method=RegisterToken.EMAIL)
      return token
    except RegisterToken.DoesNotExist:
      raise forms.ValidationError("Invalid token.")


class AuthenticationForm(forms.Form):
  """
  Base class for authenticating users. Extend this to get a form that accepts
  username/password logins.
  """
  username = forms.CharField(max_length=2048)
  password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

  error_messages = {
      'invalid_login': _("Please enter a correct %(username)s and password. "
                         "Note that both fields may be case-sensitive."),
      'inactive': _("This account is inactive."),
  }

  def __init__(self, request=None, *args, **kwargs):
    """
    The 'request' parameter is set for custom auth use by subclasses.
    The form data comes in via the standard 'data' kwarg.
    """
    self.request = request
    self.user_cache = None
    super(AuthenticationForm, self).__init__(*args, **kwargs)

    # Set the label for the "username" field.
    UserModel = get_user_model()
    self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
    if self.fields['username'].label is None:
      self.fields['username'].label = capfirst(self.username_field.verbose_name)

  def clean(self):
    username = self.cleaned_data.get('username')
    password = self.cleaned_data.get('password')

    if username and password:
      self.user_cache = authenticate(username=username,
                                     password=password)
      if self.user_cache is None:
        raise forms.ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': self.username_field.verbose_name},
        )
      else:
        self.confirm_login_allowed(self.user_cache)

    return self.cleaned_data

  def confirm_login_allowed(self, user):
    """
    Controls whether the given User may log in. This is a policy setting,
    independent of end-user authentication. This default behavior is to
    allow login by active users, and reject login by inactive users.
    If the given user cannot log in, this method should raise a
    ``forms.ValidationError``.
    If the given user may log in, this method should return None.
    """
    if not user.is_active:
      raise forms.ValidationError(
          self.error_messages['inactive'],
          code='inactive',
      )

  def get_user_id(self):
    if self.user_cache:
      return self.user_cache.id
    return None

  def get_user(self):
    return self.user_cache



class UserCreationForm(forms.ModelForm):
  """
  A form that creates a user, with no privileges, from the given username and
  password.
  """
  error_messages = {
      'duplicate_username': _("A user with that username already exists."),
      'password_mismatch': _("The two password fields didn't match."),
  }
  username = forms.RegexField(label=_("Username"), max_length=2048,
      regex=r'^[\w.@+-]+$',
      help_text=_("Required. 2048 characters or fewer. Letters, digits and "
                  "@/./+/-/_ only."),
      error_messages={
          'invalid': _("This value may contain only letters, numbers and "
                       "@/./+/-/_ characters.")})

  class Meta:
    model = User
    fields = ("username",)

  def clean_username(self):
    # Since User.username is unique, this check is redundant,
    # but it sets a nicer error message than the ORM. See #13147.
    username = self.cleaned_data["username"]
    try:
      User._default_manager.get(username=username)
    except User.DoesNotExist:
      return username
    raise forms.ValidationError(
        self.error_messages['duplicate_username'],
        code='duplicate_username',
    )

  def save(self, commit=True):
    user = super(UserCreationForm, self).save(commit=commit)
    user.set_unusable_password()
    user.save()
    return user


class UserChangeForm(forms.ModelForm):
  username = forms.RegexField(
      label=_("Username"), max_length=2048, regex=r"^[\w.@+-]+$",
      help_text=_("Required. 2048 characters or fewer. Letters, digits and "
                  "@/./+/-/_ only."),
      error_messages={
          'invalid': _("This value may contain only letters, numbers and "
                       "@/./+/-/_ characters.")})
  password = ReadOnlyPasswordHashField(label=_("Password"),
      help_text=_("Raw passwords are not stored, so there is no way to see "
                  "this user's password, but you can change the password "
                  "using <a href=\"password/\">this form</a>."))

  class Meta:
    model = User
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super(UserChangeForm, self).__init__(*args, **kwargs)
    f = self.fields.get('user_permissions', None)
    if f is not None:
      f.queryset = f.queryset.select_related('content_type')

  def clean_password(self):
    # Regardless of what the user provides, return the initial value.
    # This is done here, rather than on the field, because the
    # field does not have access to the initial value
    return self.initial["password"]


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

