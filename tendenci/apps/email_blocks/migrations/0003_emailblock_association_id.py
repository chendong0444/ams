# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_blocks', '0002_auto_20160926_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailblock',
            name='association_id',
            field=models.IntegerField(default=0),
        ),
    ]
