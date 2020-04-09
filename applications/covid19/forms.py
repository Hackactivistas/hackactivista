from .models import DiagnosisCovid19
from django import forms

class DiagnosisCovid19Form(forms.ModelForm):
    class Meta:
        model = DiagnosisCovid19
        fields = ('img','user_upload')