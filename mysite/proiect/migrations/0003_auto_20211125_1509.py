# Generated by Django 3.2.9 on 2021-11-25 15:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proiect', '0002_messages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='dateSent',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]