# Generated by Django 3.2.6 on 2023-11-14 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0036_auto_20231114_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
