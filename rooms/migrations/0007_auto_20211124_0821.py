# Generated by Django 3.2.8 on 2021-11-23 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0006_auto_20211123_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='check_in',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='room',
            name='check_out',
            field=models.TimeField(),
        ),
    ]
