# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagerprofile',
            name='user',
            field=models.OneToOneField(related_name='ImagerProfile', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
