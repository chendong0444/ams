# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('associations', '0002_association_owner'),
        ('profiles', '0009_profile_association_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='association_id',
        ),
        migrations.AddField(
            model_name='profile',
            name='current_association',
            field=models.ForeignKey(related_name='profiles_profile_current_association', on_delete=django.db.models.deletion.SET_NULL, default=None, to='associations.Association', null=True),
        ),
    ]
