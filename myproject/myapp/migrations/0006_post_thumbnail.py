# Generated by Django 4.1.3 on 2022-11-25 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]
