# Generated by Django 5.0.6 on 2024-06-15 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='shop/images/default.jpg', upload_to='shop/images'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='profile_pics/default', upload_to='profile_pics/'),
        ),
    ]
