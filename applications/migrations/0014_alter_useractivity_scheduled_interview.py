# Generated by Django 5.1.2 on 2024-11-22 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0013_alter_useractivity_action_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivity',
            name='scheduled_interview',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
