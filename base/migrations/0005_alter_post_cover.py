# Generated by Django 4.2.5 on 2023-10-22 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_post_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='cover',
            field=models.ImageField(upload_to='covers/'),
        ),
    ]