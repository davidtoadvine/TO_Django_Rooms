# Generated by Django 5.0.6 on 2024-06-25 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_person_preferences'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='preferences',
        ),
        migrations.AddField(
            model_name='person',
            name='preference',
            field=models.CharField(choices=[('preference_open', 'Open to any guest'), ('preference_mid', 'Only known guests'), ('preference_strict', 'Only members')], default='preference_open', max_length=20),
        ),
    ]
