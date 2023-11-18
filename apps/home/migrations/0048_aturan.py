# Generated by Django 3.2.6 on 2023-11-18 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0047_alter_jadwalbusm_via'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aturan',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('div_cat', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('pdf_file', models.FileField(upload_to='uploads/aturan_pdfs/')),
            ],
        ),
    ]
