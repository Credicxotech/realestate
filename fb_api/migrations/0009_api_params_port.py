# Generated by Django 4.0.1 on 2022-01-20 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fb_api', '0008_remove_api_params_post_url_api_params_post_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='api_params',
            name='port',
            field=models.IntegerField(default=None),
        ),
    ]
