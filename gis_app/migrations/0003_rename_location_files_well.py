# Generated by Django 5.1 on 2024-08-20 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gis_app', '0002_alter_files_location_delete_locations'),
    ]

    operations = [
        migrations.RenameField(
            model_name='files',
            old_name='location',
            new_name='well',
        ),
    ]
