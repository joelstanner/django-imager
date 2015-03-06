# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0005_album_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='cover',
            field=models.ImageField(null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='album',
            name='date_modified',
            field=models.DateField(default=None, auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='album',
            name='date_published',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='album',
            name='date_uploaded',
            field=models.DateField(default=None, auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='album',
            name='description',
            field=models.TextField(default=b'No Description'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='album',
            name='photos',
            field=models.ManyToManyField(related_name='album_set', to='imager_images.Photo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='album',
            name='published',
            field=models.CharField(default=b'pv', max_length=2, choices=[(b'pb', b'public'), (b'pv', b'private'), (b'sh', b'shared')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='album',
            name='title',
            field=models.CharField(default=b'No Title', max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='album',
            name='user',
            field=models.ForeignKey(related_name='album_set', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='photo',
            name='album',
            field=models.ManyToManyField(related_name='photo_set', null=True, to='imager_images.Album', blank=True),
            preserve_default=True,
        ),
    ]
