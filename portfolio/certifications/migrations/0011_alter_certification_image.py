# Generated by Django 4.1.5 on 2023-01-18 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certifications', '0010_alter_certification_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certification',
            name='image',
            field=models.CharField(max_length=100),
        ),
    ]
