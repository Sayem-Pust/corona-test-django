from django.db import models
from django.contrib.auth.models import User


class SymptomChoice(models.Model):
    symptom_choice = models.CharField(max_length=30, blank=True)

    def __unicode__(self):
        return self.symptom_choice

    def __str__(self):
        return self.symptom_choice


class AdditionalInfo(models.Model):
    additional_choice = models.CharField(max_length=30, blank=True)

    def __unicode__(self):
        return self.additional_choice

    def __str__(self):
        return self.additional_choice


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=120, blank=True, null=True)
    age = models.IntegerField(default=0)
    gender_choice = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=30, blank=True, null=True, choices=gender_choice)
    body_temperature = models.DecimalField(max_digits=7, decimal_places=2)
    symptom = models.ManyToManyField(SymptomChoice, blank=True, null=True)
    additional = models.ManyToManyField(AdditionalInfo, blank=True, null=True)
    result = models.CharField(max_length=120, blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    is_tested = models.BooleanField(default=False)
    advice = models.TextField(blank=True, null=True)
    emergency_info = models.TextField(blank=True, null=True)
    export_to_CSV = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
