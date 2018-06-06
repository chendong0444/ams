# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0002_story_video_embed_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='association_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='story',
            name='video_embed_url',
            field=models.URLField(help_text='Embed URL for a Youtube or Vimeo video', null=True, verbose_name='Embed URL', blank=True),
        ),
    ]
