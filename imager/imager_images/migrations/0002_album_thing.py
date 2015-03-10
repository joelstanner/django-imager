# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='thing',
            field=models.CharField(default=b'nothing', max_length=256),
            preserve_default=True,
        ),
    ]
