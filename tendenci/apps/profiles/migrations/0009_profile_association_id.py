# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_remove_profile_current_association_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='association_id',
            field=models.IntegerField(default=0),
        ),
    ]
