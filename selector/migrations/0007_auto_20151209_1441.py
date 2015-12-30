# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('selector', '0006_auto_20151209_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authassociationtoken',
            name='user',
            field=models.ForeignKey(related_name=b'authassociationtokens', to=settings.AUTH_USER_MODEL),
        ),
    ]
