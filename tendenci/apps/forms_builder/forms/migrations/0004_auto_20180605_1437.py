# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0003_auto_20170324_1204'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='association_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='field',
            name='field_function',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Special Functionality', choices=[(b'GroupSubscription', 'Subscribe to Group'), (b'GroupSubscriptionAuto', 'Subscribe to Group (Auto)'), (b'EmailFirstName', 'First Name'), (b'EmailLastName', 'Last Name'), (b'EmailFullName', 'Full Name'), (b'EmailPhoneNumber', 'Phone Number'), (b'Recipients', 'Email to Recipients')]),
        ),
    ]
