# Generated by Django 5.1.7 on 2025-05-21 03:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_payment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
