# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('associations', '0003_association_wechat_mp_appid'),
    ]

    operations = [
        migrations.AddField(
            model_name='association',
            name='custom_domain',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
