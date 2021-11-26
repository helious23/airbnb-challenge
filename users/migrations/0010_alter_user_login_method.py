# Generated by Django 3.2.8 on 2021-11-26 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_user_login_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='login_method',
            field=models.CharField(choices=[('email', 'E-mail'), ('github', 'Github'), ('kakao', 'Kakao'), ('naver', 'Naver')], default='email', max_length=12),
        ),
    ]