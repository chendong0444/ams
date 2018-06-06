# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meta',
            name='canonical_url',
            field=models.CharField(max_length=500, verbose_name='canonical_url', blank=True),
        ),
        migrations.AlterField(
            model_name='meta',
            name='description',
            field=models.TextField(verbose_name='description', blank=True),
        ),
        migrations.AlterField(
            model_name='meta',
            name='keywords',
            field=models.TextField(verbose_name='keywords', blank=True),
        ),
        migrations.AlterField(
            model_name='meta',
            name='title',
            field=models.CharField(max_length=200, verbose_name='title', blank=True),
        ),
    ]
