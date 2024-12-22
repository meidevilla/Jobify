# Generated by Django 5.1.2 on 2024-11-11 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0002_jobapplication_work_setup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='status',
            field=models.CharField(choices=[('Applied', 'Applied'), ('Interviewing', 'Interviewing'), ('Offer Received', 'Offer Received'), ('Rejected', 'Rejected')], default='Applied', max_length=50),
        ),
    ]