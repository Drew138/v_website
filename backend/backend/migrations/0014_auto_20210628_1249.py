# Generated by Django 3.0.7 on 2021-06-28 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_auto_20210626_2350'),
    ]

    operations = [
        migrations.AddField(
            model_name='point',
            name='severity',
            field=models.CharField(choices=[('red', 'Red'), ('green', 'Green'), ('yellow', 'Yellow'), ('black', 'Black'), ('purple', 'Purple')], default='purple', max_length=9),
        ),
        migrations.AlterUniqueTogether(
            name='point',
            unique_together={('position', 'direction', 'point_type', 'machine')},
        ),
    ]
