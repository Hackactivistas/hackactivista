from django.db import models

# Create your models here.
class TermsCondition(models.Model):
    content = models.TextField(max_length=20000)
    date_create = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = ('Términos y condiciones')

    def __str__(self):
        return 'Content'


class PrivacyPolice(models.Model):
    content = models.TextField(max_length=20000)
    date_create = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = ('Políticas de privacidad')

    def __str__(self):
        return 'Content'