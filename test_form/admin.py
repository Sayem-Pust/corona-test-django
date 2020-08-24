from django.contrib import admin
from .models import Profile, AdditionalInfo, SymptomChoice


admin.site.register(Profile)
admin.site.register(SymptomChoice)
admin.site.register(AdditionalInfo)

