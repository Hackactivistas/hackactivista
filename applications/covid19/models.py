from django.db import models
from applications.users.models import Usuario

# Create your models here.
class DiagnosisCovid19(models.Model):
	"""docstring for Diagnosis_covid_19"""
	user_upload = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	date_register = models.DateTimeField(auto_now=True)
	img = models.ImageField(upload_to='imgs-covid19', null=True)
	status_process = models.BooleanField(default=False)
	def __str__(self):
		return self.user_upload.usuario or u''