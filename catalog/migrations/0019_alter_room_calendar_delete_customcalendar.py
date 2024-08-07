# Generated by Django 5.0.6 on 2024-07-02 01:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_alter_room_calendar'),
        ('schedule', '0014_use_autofields_for_pk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='calendar',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room', to='schedule.calendar'),
        ),
        migrations.DeleteModel(
            name='CustomCalendar',
        ),
    ]
