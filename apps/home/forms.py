from django import forms
from .models import Formmodel, ProsedurM, GalleryKegiatanm, DataPoint, JadwalBusM

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

