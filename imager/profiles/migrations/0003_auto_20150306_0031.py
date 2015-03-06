# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20150304_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagerprofile',
            name='blocked',
            field=models.ManyToManyField(related_name='blockedby_set', to='profiles.ImagerProfile', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imagerprofile',
            name='follows',
            field=models.ManyToManyField(related_name='followers_set', to='profiles.ImagerProfile', blank=True),
            preserve_default=True,
        ),
    ]
