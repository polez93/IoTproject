# Generated by Django 5.0.6 on 2024-05-30 14:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensores', '0006_alter_lectura_hora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lectura',
            name='hora',
            field=models.TimeField(default=datetime.datetime(2024, 5, 30, 9, 51, 31, 454708)),
        ),
    ]