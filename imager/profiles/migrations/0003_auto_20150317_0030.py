# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('profiles', '0002_default_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='default_group',
            name='group_ptr',
        ),
        migrations.DeleteModel(
            name='Default_Group',
        ),
    ]
