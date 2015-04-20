# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wxapp', '0003_clothes'),
    ]

    operations = [
        migrations.AddField(
            model_name='clothes',
            name='test',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
    ]
