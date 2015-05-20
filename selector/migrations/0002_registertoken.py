# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('selector', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisterToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=200)),
                ('issued_at', models.DateTimeField(auto_now_add=True)),
                ('method', models.CharField(default=b'email', max_length=200, choices=[(b'email', '#method-email')])),
                ('sent', models.BooleanField(default=False)),
                ('user', models.ForeignKey(related_name=b'registertokens', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
