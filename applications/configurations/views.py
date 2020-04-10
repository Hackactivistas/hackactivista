# Create your views here.
from django.shortcuts import render
from .models import *
from django.views.generic import ListView
# Create your views here.


class TermsCondition(ListView):
    context_object_name = 'terms'
    template_name = 'terminos.html'
    queryset = TermsCondition.objects.all()

class PrivacyPolice(ListView):
    context_object_name = 'politics'
    template_name = 'politicas.html'
    queryset = PrivacyPolice.objects.all()
   