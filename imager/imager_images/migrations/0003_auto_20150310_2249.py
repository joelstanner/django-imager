# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0002_album_thing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='thing',
        ),
        migrations.AlterField(
            model_name='album',
            name='photos',
            field=models.ManyToManyField(related_name='album_set', to='imager_images.Photo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='album',
            name='profile',
            field=models.ForeignKey(related_name='album_set', to='profiles.ImagerProfile'),
            preserve_default=True,
        ),
    ]
