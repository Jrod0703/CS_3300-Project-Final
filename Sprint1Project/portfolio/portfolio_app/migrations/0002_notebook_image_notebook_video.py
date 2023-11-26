# Generated by Django 4.2.5 on 2023-11-24 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notebook',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='notebooks/images/'),
        ),
        migrations.AddField(
            model_name='notebook',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='notebooks/videos/'),
        ),
    ]
