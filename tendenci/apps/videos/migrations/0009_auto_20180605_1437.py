# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0008_auto_20170905_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='association_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='video',
            name='slug',
            field=models.SlugField(unique=True, max_length=200, verbose_name='URL Path'),
        ),
    ]
