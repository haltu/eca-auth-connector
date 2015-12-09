# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('selector', '0005_mepinassociationtoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthAssociationToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=200)),
                ('issued_at', models.DateTimeField(auto_now_add=True)),
                ('is_used', models.BooleanField(default=False)),
                ('user', models.ForeignKey(related_name=b'mepinassociationtokens', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='mepinassociationtoken',
            name='user',
        ),
        migrations.DeleteModel(
            name='MePinAssociationToken',
        ),
    ]
