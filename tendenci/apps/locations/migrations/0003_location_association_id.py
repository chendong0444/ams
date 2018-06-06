# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20170328_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='association_id',
            field=models.IntegerField(default=0),
        ),
    ]
