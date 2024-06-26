# Generated by Django 5.0.6 on 2024-06-09 23:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_alter_person_contact_email'),
        ('schedule', '0014_use_autofields_for_pk'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomEvent',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='schedule.event')),
                ('event_type', models.CharField(choices=[('occupancy', 'Occupancy'), ('availability', 'Availability')], max_length=20)),
            ],
            bases=('schedule.event',),
        ),
    ]
