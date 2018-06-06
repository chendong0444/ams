# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_auto_20180605_1419'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='current_association_id',
        ),
    ]
