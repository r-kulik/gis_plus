# Generated by Django 5.1 on 2024-08-20 10:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Companies',
            fields=[
                ('companyId', models.AutoField(primary_key=True, serialize=False)),
                ('companyName', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CurveMetrics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metricName', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Fields',
            fields=[
                ('fieldId', models.AutoField(primary_key=True, serialize=False)),
                ('fieldName', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('locationId', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('fileId', models.AutoField(primary_key=True, serialize=False)),
                ('filePath', models.FilePathField()),
                ('fileVersion', models.CharField(max_length=5)),
                ('startDepth', models.FloatField()),
                ('stopDepth', models.FloatField()),
                ('datetime', models.DateTimeField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gis_app.companies')),
                ('metrics', models.ManyToManyField(to='gis_app.curvemetrics')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gis_app.locations')),
            ],
        ),
        migrations.CreateModel(
            name='Wells',
            fields=[
                ('wellId', models.AutoField(primary_key=True, serialize=False)),
                ('wellNumber', models.TextField()),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gis_app.fields')),
            ],
        ),
        migrations.AddField(
            model_name='locations',
            name='well',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gis_app.wells'),
        ),
    ]
