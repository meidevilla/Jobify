# Generated by Django 5.1.2 on 2024-11-22 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0012_alter_useractivity_action_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivity',
            name='action_type',
            field=models.CharField(choices=[('submitted_application', 'Submitted Application'), ('interview_scheduled', 'Scheduled Interview'), ('status_changed', 'Changedd Status')], max_length=30),
        ),
    ]