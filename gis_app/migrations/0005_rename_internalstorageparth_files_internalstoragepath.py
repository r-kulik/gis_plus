# Generated by Django 5.1 on 2024-08-21 04:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gis_app', '0004_files_internalstorageparth'),
    ]

    operations = [
        migrations.RenameField(
            model_name='files',
            old_name='internalStorageParth',
            new_name='internalStoragePath',
        ),
    ]
