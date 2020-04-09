from django.shortcuts import render
import requests
import json
from django.conf import settings
from braces.views import (LoginRequiredMixin, PermissionRequiredMixin)
from django.views.generic import (ListView, UpdateView, 
								DeleteView, CreateView, TemplateView)

# Create your views here.
class DiagnosisCovid19(LoginRequiredMixin, TemplateView):
    template_name = 'covid19/diagnosis_covid_19.html'

class APIClient:
    def __init__(self):
        self.covidnet_endpoint = settings.COVIDNET_ENDPOINT
        self.covidnet_apikey = settings.COVIDNET_API_KEY
    def covidnet_post(self, path_file):
        url = self.covidnet_endpoint
        files = {'file': open(path_file, 'rb')}
        headers = {'apikey': self.covidnet_apikey}
        resp = requests.post(url, files=files, headers=headers)
        resp_json = json.loads(resp.text)
        print(resp_json)
        return resp_json.get('result')

def api_diagnosis_covid19():
	ac = APIClient()
	print(ac.covidnet_post('/home/alejandro/Desktop/prueba1.jpg'))
