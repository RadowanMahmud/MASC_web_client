# Generated by Django 4.0.6 on 2022-12-05 19:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MascEngine', '0004_alter_processlog_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processlog',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 6, 1, 43, 51, 677425)),
        ),
    ]
