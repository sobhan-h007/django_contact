from django.db import models
from django.core.validators import RegexValidator


numeric = RegexValidator(r'^[0-9]+', 'Only digit characters.')
class Contact(models.Model):
    full_name = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    relationship = models.CharField(max_length=50, null= True, blank=True )
    email = models.EmailField(max_length=255, null= True,blank=True)
    phone_number = models.PositiveIntegerField(max_length=11,blank=True, null= True,validators=[numeric])

    address = models.CharField(max_length=255, null= True, blank=True)


    def __str__(self):
        return self.full_name


