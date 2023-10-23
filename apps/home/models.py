from django.db import models
from django.utils import timezone


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
    no_prosedur = models.CharField(max_length=51)
    category_prosedur = models.CharField(max_length=100)
    file_upload = models.FileField(upload_to="uploads/")

    def __str__(self):
        return self.nama_prosedur


class Visitor(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField()
    

    def __str__(self):
        return f"{self.ip_address} - {self.timestamp}"


class GalleryKegiatanm(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='uploads/')
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class JadwalBusM(models.Model):
    id = models.AutoField(primary_key=True)
    titikStart = models.CharField(max_length=30)
    plant = models.CharField(max_length=2)
    via = models.CharField(max_length=20)
    seat = models.IntegerField(max_length=2)
    shift1 = models.CharField(max_length=5, null=True)
    shift2 = models.CharField(max_length=5, null=True)
    shift3 = models.CharField(max_length=5, null=True)

class DataPoint(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.CharField(max_length=25)
    value = models.FloatField()

    def __str__(self):
        return f"{self.date} - {self.value}"
