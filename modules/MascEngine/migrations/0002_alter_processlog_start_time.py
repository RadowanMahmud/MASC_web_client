# Generated by Django 4.0.6 on 2022-11-22 06:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MascEngine', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processlog',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 22, 12, 2, 20, 325421)),
        ),
    ]