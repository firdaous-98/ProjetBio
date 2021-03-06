# Generated by Django 3.0.5 on 2020-11-09 18:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fastq_files', models.FileField(blank=True, upload_to='data/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['gz'])])),
                ('mapping_file', models.FileField(upload_to='data/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['txt'])])),
                ('sample_size', models.IntegerField(default=50000)),
                ('min_otu_freq', models.FloatField(default=0.001)),
                ('p_perc_identity', models.FloatField(default=0.97)),
                ('dateDebut', models.DateField()),
                ('dateFin', models.DateField()),
                ('user', models.TextField()),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.TextField()),
                ('nbr_of_analysis', models.IntegerField()),
            ],
        ),
    ]
