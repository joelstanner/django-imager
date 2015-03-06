# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0002_photo_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='photo',
            field=models.ImageField(upload_to=b'', blank=True),
            preserve_default=True,
        ),
    ]
