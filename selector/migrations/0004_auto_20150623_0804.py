# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('selector', '0003_auto_20150525_1719'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registertoken',
            old_name='sent',
            new_name='is_sent',
        ),
        migrations.AddField(
            model_name='registertoken',
            name='is_used',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='registertoken',
            name='issuer_auth_method',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registertoken',
            name='issuer_oid',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
