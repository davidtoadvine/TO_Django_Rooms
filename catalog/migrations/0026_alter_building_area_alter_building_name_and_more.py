# Generated by Django 5.0.6 on 2024-11-30 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0025_building_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='area',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='building',
            name='name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='section',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
