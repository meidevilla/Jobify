# Generated by Django 5.1.2 on 2024-12-04 12:39

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0019_userprofile_current_streak_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='date_applied',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]