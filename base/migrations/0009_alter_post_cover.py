# Generated by Django 4.2.5 on 2023-10-22 14:58

import base.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_post_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to=base.models.rename),
        ),
    ]
