# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case_studies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='casestudy',
            name='association_id',
            field=models.IntegerField(default=0),
        ),
    ]
