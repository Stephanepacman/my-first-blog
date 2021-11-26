from django.contrib import admin
from .models import Equipement, Animal

# Register your models here.
admin.site.register(Animal)
admin.site.register(Equipement)