# Generated by Django 5.0.6 on 2024-07-03 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_profile_options_profile_bio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='DEFAULTS/profile_default', upload_to='images/'),
        ),
    ]
