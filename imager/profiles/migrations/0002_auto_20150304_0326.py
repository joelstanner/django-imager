# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagerprofile',
            name='following',
        ),
        migrations.AddField(
            model_name='imagerprofile',
            name='follows',
            field=models.ManyToManyField(related_name='follows_rel_+', to='profiles.ImagerProfile'),
            preserve_default=True,
        ),
    ]
