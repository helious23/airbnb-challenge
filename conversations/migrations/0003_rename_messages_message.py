# Generated by Django 3.2.8 on 2021-11-23 05:52

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conversations', '0002_rename_mesages_messages'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Messages',
            new_name='Message',
        ),
    ]
