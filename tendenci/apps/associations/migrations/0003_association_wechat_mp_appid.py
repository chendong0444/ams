# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('associations', '0002_association_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='association',
            name='wechat_mp_appid',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
