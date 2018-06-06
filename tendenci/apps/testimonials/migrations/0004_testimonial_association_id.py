# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testimonials', '0003_auto_20171023_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonial',
            name='association_id',
            field=models.IntegerField(default=0),
        ),
    ]
