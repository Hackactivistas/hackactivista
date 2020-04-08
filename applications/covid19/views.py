from django.shortcuts import render
from braces.views import (LoginRequiredMixin, 
	PermissionRequiredMixin)
from django.views.generic import (ListView, UpdateView, 
	DeleteView, CreateView, TemplateView)

# Create your views here.


class DiagnosisCovid19(LoginRequiredMixin, TemplateView):
    template_name = 'covid19/diagnosis_covid_19.html'
