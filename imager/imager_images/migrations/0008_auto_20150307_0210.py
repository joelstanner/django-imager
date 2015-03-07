# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20150306_0213'),
        ('imager_images', '0007_auto_20150306_0518'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='user',
        ),
        migrations.AddField(
            model_name='album',
            name='profile',
            field=models.ForeignKey(related_name='album_set', default=None, to='profiles.ImagerProfile'),
            preserve_default=False,
        ),
    ]
