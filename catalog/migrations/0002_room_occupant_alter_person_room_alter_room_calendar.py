# Generated by Django 5.0.6 on 2024-06-09 13:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
        ('schedule', '0014_use_autofields_for_pk'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='occupant',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room_occupant', to='catalog.person'),
        ),
        migrations.AlterField(
            model_name='person',
            name='room',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='person_room', to='catalog.room'),
        ),
        migrations.AlterField(
            model_name='room',
            name='calendar',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room_calendar', to='schedule.calendar'),
        ),
    ]
