# Generated by Django 5.0.6 on 2024-06-23 05:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_person_parent_person_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='owner',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room', to='catalog.person'),
        ),
    ]
