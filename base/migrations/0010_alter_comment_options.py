# Generated by Django 4.2.5 on 2023-11-04 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_post_cover'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created']},
        ),
    ]
