# Generated by Django 3.2.6 on 2023-11-07 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_auto_20231107_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menukantinm',
            name='file',
            field=models.FileField(upload_to='uploads/menuKantin/'),
        ),
        migrations.AlterField(
            model_name='pengumumanypmim',
            name='file_pengumuman',
            field=models.FileField(upload_to='uploads/pengumuman/'),
        ),
    ]
