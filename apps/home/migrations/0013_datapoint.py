# Generated by Django 3.2.6 on 2023-10-12 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_delete_datapoint'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataPoint',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.CharField(max_length=25)),
                ('value', models.FloatField()),
            ],
        ),
    ]
