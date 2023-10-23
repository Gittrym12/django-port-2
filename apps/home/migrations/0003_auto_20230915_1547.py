# Generated by Django 3.2.6 on 2023-09-15 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_formprosedurm_category_prosedur'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProsedurM',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nama_prosedur', models.CharField(max_length=100)),
                ('no_prosedur', models.CharField(max_length=51)),
                ('category_prosedur', models.CharField(max_length=100)),
                ('file_upload', models.FileField(upload_to='uploads/')),
            ],
        ),
        migrations.DeleteModel(
            name='FormProsedurm',
        ),
    ]
