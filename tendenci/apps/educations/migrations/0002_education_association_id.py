# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('educations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='education',
            name='association_id',
            field=models.IntegerField(default=0),
        ),
    ]
