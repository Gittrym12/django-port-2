from django import forms
from .models import Formmodel, ProsedurM, GalleryKegiatanm, DataPoint, JadwalBusM, menuKantinM
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


class DataPointF(forms.ModelForm):
    class Meta:
        model = DataPoint
        fields = "__all__"


class JadwalBusF(forms.ModelForm):
    class Meta:
        model = JadwalBusM
        fields = "__all__"


def validate_file_extension(value):
    if not value.name.endswith('.xlsx') and not value.name.endswith('.csv'):
        raise ValidationError('Only XLSX or CSV files are allowed.')

class menuKantinF(forms.ModelForm):
    class Meta:
        model = menuKantinM
        fields = "__all__"

    file = forms.FileField(validators=[validate_file_extension])
