# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wxapp', '0006_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='clothes',
            name='user',
            field=models.ForeignKey(default=1, to='wxapp.user'),
            preserve_default=False,
        ),
    ]
