# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0006_auto_20151115_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='association_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='language',
            field=models.CharField(default=b'zh', max_length=10, verbose_name='Language', blank=True, choices=[(b'en', b'English'), (b'zh', b'Simplified Chinese')]),
        ),
        migrations.AlterField(
            model_name='topic',
            name='user',
            field=models.ForeignKey(verbose_name='Owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
