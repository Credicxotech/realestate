# Generated by Django 4.0.2 on 2022-03-02 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fb_api', '0017_get_cookies_api_params'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testing_api',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(default=None, max_length=50)),
            ],
        ),
    ]