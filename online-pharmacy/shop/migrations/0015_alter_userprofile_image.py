# Generated by Django 5.0.6 on 2024-06-15 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_alter_userprofile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='/media/profile_pics/default.jpg', upload_to='profile_pics/'),
        ),
    ]
