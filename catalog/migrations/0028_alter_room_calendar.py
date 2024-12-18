# Generated by Django 5.0.6 on 2024-12-01 19:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0027_alter_room_calendar'),
        ('schedule', '0014_use_autofields_for_pk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='calendar',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room', to='schedule.calendar'),
        ),
    ]
