# Generated by Django 4.0.1 on 2022-01-09 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fb_api', '0003_api_params_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='api_params',
            name='cookies',
            field=models.CharField(max_length=10000),
        ),
    ]
