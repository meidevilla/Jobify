# Generated by Django 5.1.2 on 2024-11-11 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='work_setup',
            field=models.CharField(choices=[('Full FTF', 'Full FTF'), ('Hybrid', 'Hybrid'), ('Remote', 'Remote')], default='Full FTF', max_length=50),
        ),
    ]
