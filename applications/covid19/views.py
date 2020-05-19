from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse, HttpResponse
import requests
import json
from django.conf import settings
from braces.views import (LoginRequiredMixin, PermissionRequiredMixin)
from django.views.generic import (ListView, UpdateView, 
								DeleteView, CreateView, TemplateView)
from .forms import DiagnosisCovid19Form

# Create your views here.
# class DiagnosisCovid19(LoginRequiredMixin, TemplateView):
#     template_name = 'covid19/diagnosis_covid_19.html'

class APIClient:
    def __init__(self):
        self.covidnet_endpoint = settings.COVIDNET_ENDPOINT
        self.covidnet_apikey = settings.COVIDNET_API_KEY
    def covidnet_post(self, path_file):
    	try:
    		url = self.covidnet_endpoint
    		files = {'file': open(path_file, 'rb')}
    		headers = {'apikey': self.covidnet_apikey}
    		resp = requests.post(url, files=files, headers=headers)
    		resp_json = json.loads(resp.text)
    		return resp_json.get('result')
    	except Exception as e:
    		print ('Error api>', e)
    		return 
# def api_diagnosis_covid19():
# 	ac = APIClient()
# 	print(ac.covidnet_post('/home/alejandro/Desktop/prueba1.jpg'))

class DiagnosisCovid19(View):
    def get(self, request):
        return render(self.request, 'covid19/diagnosis_covid_19.html')

    def post(self, request):
        if request.is_ajax():
        	form = DiagnosisCovid19Form(self.request.POST, self.request.FILES)
        	if form.is_valid():
        		photo = form.save()
        		ac = APIClient()
        		get_data_api_img = ac.covidnet_post('public/media/' + photo.img.name)
        		data = {'is_valid': True, 'name': photo.img.name, 
        			'url': photo.img.url, 'data_result':get_data_api_img}
        	else:
        		data = {'is_valid': False}
        	return JsonResponse(data)
        else:
            return redirect('/')