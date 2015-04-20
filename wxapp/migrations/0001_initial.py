# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='clothes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, blank=True)),
                ('category', models.CharField(blank=True, max_length=2, choices=[(b'1', b'business'), (b'2', b'business casual'), (b'3', b'casual'), (b'4', b'sport')])),
                ('season', models.CharField(blank=True, max_length=1, choices=[(b'1', b'spring and autumn'), (b'2', b'summer'), (b'3', b'winter')])),
                ('tag', models.CharField(max_length=200, blank=True)),
                ('choose_count', models.SmallIntegerField(default=0)),
                ('add_date', models.DateField(auto_now_add=True)),
                ('image_filename', models.CharField(max_length=20, blank=True)),
            ],
        ),
    ]
