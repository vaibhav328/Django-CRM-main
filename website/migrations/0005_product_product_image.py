# Generated by Django 4.2.9 on 2024-01-28 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, null=True, upload_to='product_image/'),
        ),
    ]
