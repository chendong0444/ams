# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tendenci.apps.user_groups.utils
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='association_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='photoset',
            name='association_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='image',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=tendenci.apps.user_groups.utils.get_default_group, blank=True, to='user_groups.Group', null=True),
        ),
        migrations.AlterField(
            model_name='photoset',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=tendenci.apps.user_groups.utils.get_default_group, to='user_groups.Group', null=True),
        ),
        migrations.AlterField(
            model_name='watermark',
            name='image',
            field=models.ImageField(upload_to=b'//cdn.ams365.cn/wwwams365cn_dev/media//watermarks', verbose_name='image'),
        ),
    ]
