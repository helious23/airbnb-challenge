# Generated by Django 3.2.8 on 2021-11-22 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0003_auto_20211122_1718'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='amenity',
            options={'verbose_name_plural': 'Amenities'},
        ),
        migrations.AlterModelOptions(
            name='facility',
            options={'verbose_name_plural': 'Facilities'},
        ),
        migrations.AlterModelOptions(
            name='houserule',
            options={'verbose_name': 'House Rule'},
        ),
        migrations.AlterModelOptions(
            name='roomtype',
            options={'ordering': ['created'], 'verbose_name': 'Room Type'},
        ),
        migrations.AlterField(
            model_name='room',
            name='amenities',
            field=models.ManyToManyField(blank=True, related_name='rooms', to='rooms.Amenity'),
        ),
        migrations.AlterField(
            model_name='room',
            name='facilities',
            field=models.ManyToManyField(blank=True, related_name='rooms', to='rooms.Facility'),
        ),
        migrations.AlterField(
            model_name='room',
            name='house_rules',
            field=models.ManyToManyField(blank=True, related_name='rooms', to='rooms.HouseRule'),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('caption', models.CharField(max_length=120)),
                ('file', models.ImageField(upload_to='')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='rooms.room')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]