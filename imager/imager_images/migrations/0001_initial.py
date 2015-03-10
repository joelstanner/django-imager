# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'No Title', max_length=256)),
                ('description', models.TextField(default=b'No Description')),
                ('cover', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('date_uploaded', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateField(auto_now=True)),
                ('date_published', models.DateField(null=True)),
                ('published', models.CharField(default=b'pv', max_length=2, choices=[(b'pb', b'public'), (b'pv', b'private'), (b'sh', b'shared')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('title', models.CharField(default=b'No Title', max_length=256)),
                ('description', models.TextField(default=b'No Description')),
                ('date_uploaded', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateField(auto_now=True)),
                ('date_published', models.DateField(null=True)),
                ('published', models.CharField(default=b'pv', max_length=2, choices=[(b'pb', b'public'), (b'pv', b'private'), (b'sh', b'shared')])),
                ('album', models.ManyToManyField(related_name='photo_set', null=True, to='imager_images.Album', blank=True)),
                ('profile', models.ForeignKey(related_name='photo_set', to='profiles.ImagerProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='album',
            name='photos',
            field=models.ManyToManyField(related_name='album_set', null=True, to='imager_images.Photo', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='album',
            name='profile',
            field=models.ForeignKey(related_name='album_set', default=None, to='profiles.ImagerProfile'),
            preserve_default=True,
        ),
    ]
