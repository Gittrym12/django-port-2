# Generated by Django 3.2.6 on 2023-11-14 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0034_rename_value_datapoint_indexs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menukantinm',
            name='file',
            field=models.FileField(upload_to='uploads/menuKantin'),
        ),
        migrations.AlterField(
            model_name='pengumumanypmim',
            name='file_pengumuman',
            field=models.FileField(upload_to='uploads/pengumuman'),
        ),
        migrations.AlterField(
            model_name='pengumumanypmim',
            name='no_pengumuman',
            field=models.CharField(max_length=3),
        ),
    ]
