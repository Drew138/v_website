# Generated by Django 3.0.7 on 2021-05-21 15:29

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='machine',
            name='identifier',
        ),
        migrations.AlterField(
            model_name='company',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company', to='backend.City'),
        ),
        migrations.AlterField(
            model_name='company',
            name='phone',
            field=models.CharField(default='', max_length=17, validators=[django.core.validators.RegexValidator(message='El número de teléfono debe ser ingresado en el formato: (+xxx) xxx xxxx ext xxx siendo el código de área y la extensión opcionales.', regex='^((\\(\\+?\\d{2,3}\\))|(\\+?\\d{2,3})[\\s-])?\\d{3}[\\s-]\\d{4}([\\s-]ext[\\s-]\\d{1,3})?$')]),
        ),
        migrations.AlterField(
            model_name='vibrouser',
            name='celphone',
            field=models.CharField(default='', max_length=20, validators=[django.core.validators.RegexValidator(message='El número de celular debe ser ingresado en el formato: (+xxx) xxx xxxx xxxx siendo el código de país opcional', regex='^(((\\(\\+?\\d{2,3}\\))|(\\+?\\d{2,3}))[\\s-])?\\d{3}[\\s-]\\d{3}[\\s-]\\d{4}$')]),
        ),
        migrations.AlterField(
            model_name='vibrouser',
            name='phone',
            field=models.CharField(default='', max_length=17, validators=[django.core.validators.RegexValidator(message='El número de teléfono debe ser ingresado en el formato: (+xxx) xxx xxxx ext xxx siendo el código de área y la extensión opcionales.', regex='^((\\(\\+?\\d{2,3}\\))|(\\+?\\d{2,3})[\\s-])?\\d{3}[\\s-]\\d{4}([\\s-]ext[\\s-]\\d{1,3})?$')]),
        ),
    ]
