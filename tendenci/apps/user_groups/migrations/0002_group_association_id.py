# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='association_id',
            field=models.IntegerField(default=0),
        ),
    ]
