# Generated by Django 3.0.3 on 2020-02-25 12:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0008_auto_20200213_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='attendance',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]