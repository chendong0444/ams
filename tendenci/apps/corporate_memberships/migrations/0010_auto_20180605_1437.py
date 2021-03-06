# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corporate_memberships', '0009_auto_20170803_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='corpmembership',
            name='association_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='corpmembershipapp',
            name='association_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='corporatemembershiptype',
            name='association_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='corpprofile',
            name='association_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='freepassesstat',
            name='association_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='corporatemembershiptype',
            name='above_cap_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, blank=True, help_text='Price for members who join above cap.', null=True, verbose_name='Price if join above cap'),
        ),
        migrations.AlterField(
            model_name='corporatemembershiptype',
            name='allow_above_cap',
            field=models.BooleanField(default=False, help_text='If Apply cap is checked, check this box to allow additional members to join above cap.', verbose_name='Allow above cap'),
        ),
        migrations.AlterField(
            model_name='notice',
            name='notice_type',
            field=models.CharField(max_length=20, verbose_name='For Notice Type', choices=[(b'approve_join', 'Join Approval Date'), (b'disapprove_join', 'Join Disapproval Date'), (b'approve_renewal', 'Renewal Approval Date'), (b'disapprove_renewal', 'Renewal Disapproval Date'), (b'expiration', 'Expiration Date')]),
        ),
    ]
