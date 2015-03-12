# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0004_auto_20150311_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='photos',
            field=models.ManyToManyField(related_name='album_set', null=True, to='imager_images.Photo', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='photo',
            name='album',
            field=models.ManyToManyField(related_name='photo_set', null=True, to='imager_images.Album', blank=True),
            preserve_default=True,
        ),
    ]
