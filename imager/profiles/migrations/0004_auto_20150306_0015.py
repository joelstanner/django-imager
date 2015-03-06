# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20150306_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagerprofile',
            name='follows',
            field=models.ManyToManyField(related_name='followers_set', to='profiles.ImagerProfile', blank=True),
            preserve_default=True,
        ),
    ]
