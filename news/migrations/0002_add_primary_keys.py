# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='id',
        ),
        migrations.RemoveField(
            model_name='feed',
            name='id',
        ),
        migrations.AlterField(
            model_name='article',
            name='url',
            field=models.URLField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='feed',
            name='url',
            field=models.URLField(primary_key=True, serialize=False),
        ),
    ]
