from django.db import models

# Create your models here.

# class SeoEvento(models.Model):
# 	"""docstring for Seo"""
# 	keyword = models.CharField(max_length=450)
# 	# author = models.CharField(max_length=250, null=True)
# 	# url_canonical = models.URLField(max_length=450,null=True)
# 	title = models.CharField(max_length=450, null=True, blank=True)
# 	description = models.TextField(max_length=650, null=True, blank=True)
# 	# image_url = models.URLField(max_length=250, null=True, blank=True)
# 	published_time = models.DateTimeField(auto_now=True)
# 	modified_time = models.DateTimeField(auto_now=True)
# 	evento = models.OneToOneField(Evento, on_delete=models.CASCADE, null=True)

# 	def __str__(self):
# 		return "%s - %s" %  (self.keyword, self.evento) or u''