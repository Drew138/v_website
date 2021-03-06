# Generated by Django 3.0.7 on 2021-06-09 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20210607_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='picture',
            field=models.ImageField(default='profile/companies/default.png', upload_to='profile/companies'),
        ),
        migrations.AlterField(
            model_name='vibrouser',
            name='picture',
            field=models.ImageField(default='profile/users/default.png', upload_to='profile/users'),
        ),
    ]
