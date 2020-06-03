# Generated by Django 3.0.6 on 2020-06-03 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0006_auto_20200603_0328'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_date', models.DateField(auto_now=True)),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='record.EmployeeDetail')),
                ('product_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='record.Product')),
            ],
        ),
    ]