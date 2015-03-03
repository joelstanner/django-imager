# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(unique=True, max_length=255)),
                ('picture', models.FileField(max_length=255, upload_to=b'')),
                ('phone', models.CharField(max_length=20)),
                ('birthday', models.DateField()),
                ('name_piv', models.BooleanField(default=True)),
                ('email_piv', models.BooleanField(default=True)),
                ('picture_piv', models.BooleanField(default=True)),
                ('phone_piv', models.BooleanField(default=True)),
                ('birthday_piv', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
