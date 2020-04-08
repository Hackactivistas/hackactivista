from django.shortcuts import render
from braces.views import (LoginRequiredMixin, 
	PermissionRequiredMixin)
from django.views.generic import (ListView, UpdateView, 
	DeleteView, CreateView, TemplateView)
import requests

# Create your views here.


class DiagnosisCovid19(LoginRequiredMixin, TemplateView):
    template_name = 'covid19/diagnosis_covid_19.html'


def api_diagnosis_covid19():

	url = "http://ec2-18-212-109-235.compute-1.amazonaws.com/covidnet/imgxrays"

	payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data;\
	 		name=\"file\"; filename=\"prueba1.jpg\"\r\n\
	 		Content-Type: image/jpeg\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
	headers = {
	    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
	    'apikey': settings.api_diagnosis_covid19.get('apikey'),
	    'cache-control': "no-cache",
	    'postman-token': "20659d89-7f2a-c2a8-563e-8a5805fede03"
	    }

	response = requests.request("POST", url, data=payload, headers=headers)

	print(response.text)