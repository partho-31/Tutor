# Generated by Django 5.1.7 on 2025-05-10 14:42

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0003_tuition_course_content_tuition_duration_tuition_fee_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tuition',
            name='image',
            field=cloudinary.models.CloudinaryField(default='null', max_length=255),
            preserve_default=False,
        ),
    ]
