# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagerprofile',
            name='blocked',
            field=models.ManyToManyField(related_name='blocked_rel_+', to='profiles.ImagerProfile', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imagerprofile',
            name='follows',
            field=models.ManyToManyField(to='profiles.ImagerProfile', blank=True),
            preserve_default=True,
        ),
    ]
