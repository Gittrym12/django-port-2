from django import forms
from .models import Formmodel, ProsedurM, GalleryKegiatanm, JadwalBusM, menuKantinM, Announcement, DataKehadiran, Aturan
from django.core.exceptions import ValidationError

class FormmodelForm(forms.ModelForm):
    class Meta:
        model = Formmodel
        fields = "__all__"

class FormProsedur(forms.ModelForm):
    class Meta:
        model = ProsedurM
        fields = "__all__"


class GalleryKegiatanForm(forms.ModelForm):
    class Meta:
        model = GalleryKegiatanm
        fields = ['title', 'image']  # Include the fields you want in the form


class JadwalBusF(forms.ModelForm):
    class Meta:
        model = JadwalBusM
        fields = '__all__'



def validate_file_extension(value):
    if not value.name.endswith('.xlsx') and not value.name.endswith('.csv'):
        raise ValidationError('Only XLSX or CSV files are allowed.')

class menuKantinF(forms.ModelForm):
    class Meta:
        model = menuKantinM
        fields = "__all__"

    file = forms.FileField(validators=[validate_file_extension])


class AnnouncementForm(forms.ModelForm):
    start_date = forms.DateField(label='Start Date', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Announcement
        fields = ['catThn', 'nama_pengumuman', 'tanggal_upload', 'file_pengumuman']
        widgets = {
            'tanggal_upload': forms.DateInput(attrs={'type': 'date'}),
        }


class DataKehadiranForm(forms.ModelForm):
    class Meta:
        model = DataKehadiran
        fields = '__all__'

class AturanForm(forms.ModelForm):
    class Meta:
        model = Aturan
        fields = ['title', 'description', 'pdf_file']