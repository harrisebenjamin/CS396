# Generated by Django 4.1 on 2023-11-28 23:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Education', '0002_course'),
        ('Lessons', '0012_alter_studentscore_attemptnumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentscore',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Education.course'),
        ),
    ]
