# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wxapp', '0004_clothes_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clothes',
            name='test',
        ),
    ]
