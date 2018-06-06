# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speakers', '0002_auto_20150827_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='speaker',
            name='association_id',
            field=models.IntegerField(default=0),
        ),
    ]
