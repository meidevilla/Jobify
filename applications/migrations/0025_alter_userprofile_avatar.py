# Generated by Django 5.1.2 on 2024-12-13 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0024_alter_userprofile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='avatars/default_avatar.jpg', upload_to='avatars/'),
        ),
    ]
