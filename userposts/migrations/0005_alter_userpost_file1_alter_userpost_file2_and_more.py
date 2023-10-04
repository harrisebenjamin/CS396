# Generated by Django 4.1 on 2023-10-04 03:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("userposts", "0004_userpost_file1_userpost_file2_userpost_file3"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userpost",
            name="file1",
            field=models.FileField(blank=True, null=True, upload_to="documents/"),
        ),
        migrations.AlterField(
            model_name="userpost",
            name="file2",
            field=models.FileField(blank=True, null=True, upload_to="documents/"),
        ),
        migrations.AlterField(
            model_name="userpost",
            name="file3",
            field=models.FileField(blank=True, null=True, upload_to="documents/"),
        ),
    ]
