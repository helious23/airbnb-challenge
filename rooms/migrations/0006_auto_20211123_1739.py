# Generated by Django 3.2.8 on 2021-11-23 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0005_alter_photo_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='check_in',
            field=models.TimeField(verbose_name='%H:%M'),
        ),
        migrations.AlterField(
            model_name='room',
            name='check_out',
            field=models.TimeField(verbose_name='%H:%M'),
        ),
    ]
