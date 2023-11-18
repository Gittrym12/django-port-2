from django.db import models
from django.utils import timezone
from django.urls import reverse

class Formmodel(models.Model):
    id = models.AutoField(primary_key=True)
    nama_form = models.CharField(max_length=100)
    no_form = models.CharField(max_length=51)
    category_form = models.CharField(max_length=100)
    file_upload = models.FileField(upload_to="uploads/")

    def __str__(self):
        return self.nama_form

class ProsedurM(models.Model):
    id = models.AutoField(primary_key=True)
    nama_prosedur = models.CharField(max_length=100)
    category_prosedur = models.CharField(max_length=100)
    file_upload = models.FileField(upload_to="uploads/prosedur")

    def __str__(self):
        return self.nama_prosedur

class Visitor(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField()
    def __str__(self):
        return f"{self.ip_address} - {self.timestamp}"
class GalleryKegiatanm(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="uploads/kegiatan")
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class JadwalBusM(models.Model):
    id = models.AutoField(primary_key=True)
    titikStart = models.CharField(max_length=30)
    plant = models.CharField(max_length=2)
    via = models.CharField(max_length=55)
    seat = models.IntegerField()
    shift1 = models.CharField(max_length=5, null=True)
    shift2 = models.CharField(max_length=5, null=True)
    shift3 = models.CharField(max_length=5, null=True)


class menuKantinM(models.Model):
    id = models.AutoField(primary_key=True)
    nama_file = models.CharField(max_length=35)
    file = models.FileField(upload_to="uploads/menuKantin")
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Announcement(models.Model):
    id = models.AutoField(primary_key=True)
    catThn = models.CharField(max_length=5)
    nama_pengumuman = models.CharField(max_length=255)
    tanggal_upload = models.DateField()
    file_pengumuman = models.FileField(upload_to='uploads/pengumuman')

    def __str__(self):
        return self.nama_pengumuman


class DataKehadiran(models.Model):
    id = models.AutoField(primary_key=True)
    Bulan = models.CharField(max_length=255)
    divisi = models.CharField(max_length=45)
    image = models.ImageField(upload_to='images/kehadiran/')
    tanggal = models.DateField()
    keterangan = models.TextField()

    def __str__(self):
        return self.Bulan

class Aturan(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    div_cat = models.CharField(max_length=30)
    description = models.TextField()
    pdf_file = models.FileField(upload_to='uploads/aturan_pdfs/')

    def __str__(self):
        return self.title
