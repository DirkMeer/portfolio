# Generated by Django 4.1.5 on 2023-01-17 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certification',
            name='image',
            field=models.FilePathField(path='certifications/static/img'),
        ),
    ]
