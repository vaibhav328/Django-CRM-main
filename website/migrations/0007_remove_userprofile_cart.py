# Generated by Django 4.2.9 on 2024-01-31 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_userprofile_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='cart',
        ),
    ]
