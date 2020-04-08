from django.conf.urls import url
from .views import *

# from django.views.static.
urlpatterns = [
    url(r'^$', DiagnosisCovid19.as_view(), name='p_diagnosis_covid_19'),
]
