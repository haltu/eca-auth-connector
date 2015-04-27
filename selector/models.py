
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core import validators
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
  pass


