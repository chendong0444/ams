# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0007_membershipdefault_auto_renew'),
    ]

    operations = [
        migrations.AddField(
            model_name='membershipapp',
            name='association_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='membershipdefault',
            name='association_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='membershiptype',
            name='association_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='notice',
            name='notice_type',
            field=models.CharField(max_length=20, verbose_name='For Notice Type', choices=[(b'join', 'Join Date'), (b'renewal', 'Renewal Date'), (b'expiration', 'Expiration Date'), (b'approve', 'Join Approval Date'), (b'disapprove', 'Join Disapproval Date'), (b'approve_renewal', 'Renewal Approval Date'), (b'disapprove_renewal', 'Renewal Disapproval Date')]),
        ),
    ]
