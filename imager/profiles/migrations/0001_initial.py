# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagerProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.ImageField(upload_to=b'', blank=True)),
                ('phone', models.CharField(default=b'No Phone', max_length=20)),
                ('birthday', models.DateField(default=datetime.date.today)),
                ('name_priv', models.BooleanField(default=True)),
                ('email_priv', models.BooleanField(default=True)),
                ('picture_priv', models.BooleanField(default=True)),
                ('phone_priv', models.BooleanField(default=True)),
                ('birthday_priv', models.BooleanField(default=True)),
                ('blocked', models.ManyToManyField(related_name='blocked_rel_+', to='profiles.ImagerProfile')),
                ('follows', models.ManyToManyField(to='profiles.ImagerProfile')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
