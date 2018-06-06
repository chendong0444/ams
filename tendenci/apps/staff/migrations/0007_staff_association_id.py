# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0006_auto_20180126_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='association_id',
            field=models.IntegerField(default=0),
        ),
    ]
