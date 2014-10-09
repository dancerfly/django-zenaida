# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hints', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dismissed',
            name='key',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='dismissed',
            unique_together=set([('key', 'user')]),
        ),
    ]
