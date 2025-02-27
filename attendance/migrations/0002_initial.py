# Generated by Django 5.1.1 on 2024-10-12 12:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('attendance', '0001_initial'),
        ('faculty', '0001_initial'),
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='faculty.subject'),
        ),
        migrations.AddField(
            model_name='attendancereport',
            name='attendance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.attendance'),
        ),
        migrations.AddField(
            model_name='attendancereport',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='student.student'),
        ),
    ]
