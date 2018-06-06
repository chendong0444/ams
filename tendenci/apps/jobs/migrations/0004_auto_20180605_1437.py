# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tagging.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_auto_20170910_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='association_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='job',
            name='code',
            field=models.CharField(max_length=50, verbose_name='Code', blank=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='computer_skills',
            field=models.TextField(verbose_name='Computer skills', blank=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='contact_method',
            field=models.TextField(verbose_name='Contact method', blank=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='education',
            field=models.TextField(verbose_name='Education', blank=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='experience',
            field=models.TextField(verbose_name='Experience', blank=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='is_agency',
            field=models.BooleanField(default=False, verbose_name='Is agency'),
        ),
        migrations.AlterField(
            model_name='job',
            name='job_url',
            field=models.CharField(max_length=300, verbose_name='Job url', blank=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='level',
            field=models.CharField(max_length=50, verbose_name='Level', blank=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='location',
            field=models.CharField(max_length=500, null=True, verbose_name='Location', blank=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='period',
            field=models.CharField(max_length=50, verbose_name='Period', blank=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='position_reports_to',
            field=models.CharField(max_length=200, verbose_name='Position reports to', blank=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='salary_from',
            field=models.CharField(max_length=50, verbose_name='Salary from', blank=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='salary_to',
            field=models.CharField(max_length=50, verbose_name='Salary to', blank=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='skills',
            field=models.TextField(verbose_name='Skills', blank=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='tags',
            field=tagging.fields.TagField(max_length=255, verbose_name='Tags', blank=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='title',
            field=models.CharField(max_length=250, verbose_name='Title'),
        ),
    ]
