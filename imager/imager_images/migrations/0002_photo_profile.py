# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20150304_2333'),
        ('imager_images', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='profile',
            field=models.ForeignKey(default=None, to='profiles.ImagerProfile'),
            preserve_default=False,
        ),
    ]
