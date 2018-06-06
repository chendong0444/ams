# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('help_files', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='helpfile',
            name='association_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='helpfile',
            name='is_faq',
            field=models.BooleanField(default=False, verbose_name='Is FAQ'),
        ),
        migrations.AlterField(
            model_name='helpfile',
            name='is_featured',
            field=models.BooleanField(default=False, verbose_name='Is Featured'),
        ),
        migrations.AlterField(
            model_name='helpfile',
            name='is_video',
            field=models.BooleanField(default=False, verbose_name='Is Video'),
        ),
        migrations.AlterField(
            model_name='helpfile',
            name='level',
            field=models.CharField(default=b'basic', max_length=100, verbose_name='Level', choices=[(b'basic', 'basic'), (b'intermediate', 'intermediate'), (b'advanced', 'advanced'), (b'expert', 'expert')]),
        ),
        migrations.AlterField(
            model_name='helpfile',
            name='question',
            field=models.CharField(max_length=500, verbose_name='Question'),
        ),
    ]
