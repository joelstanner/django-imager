# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0003_auto_20150310_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='album',
            field=models.ManyToManyField(related_name='photo_set', to='imager_images.Album'),
            preserve_default=True,
        ),
    ]
