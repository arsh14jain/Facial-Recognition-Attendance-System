# Generated by Django 3.0.6 on 2020-06-03 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0008_auto_20200603_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='attendance_date',
            field=models.DateField(),
        ),
    ]
