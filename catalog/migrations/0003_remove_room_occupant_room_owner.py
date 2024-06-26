# Generated by Django 5.0.6 on 2024-06-09 21:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_room_occupant_alter_person_room_alter_room_calendar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='occupant',
        ),
        migrations.AddField(
            model_name='room',
            name='owner',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room_owner', to='catalog.person'),
        ),
    ]
