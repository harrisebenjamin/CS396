# Generated by Django 4.1 on 2023-11-04 01:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Education', '0002_course'),
        ('userposts', '0005_alter_userpost_file1_alter_userpost_file2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpost',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Education.course'),
            preserve_default=False,
        ),
    ]
