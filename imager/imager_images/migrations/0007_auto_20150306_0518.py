# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0006_auto_20150306_0338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='profile',
            field=models.ForeignKey(related_name='photo_set', to='profiles.ImagerProfile'),
            preserve_default=True,
        ),
    ]
