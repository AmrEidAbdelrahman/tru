from django.db import models
from rest_framework_api_key.models import APIKey

# Create your models here.

class APICallLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    api_key = models.ForeignKey(APIKey, on_delete=models.SET_NULL, null=True, blank=True)
    national_id = models.CharField(max_length=14)
    is_valid = models.BooleanField()
    extracted_data = models.JSONField(null=True, blank=True)
    response_status = models.IntegerField()

    def __str__(self):
        return f"{self.timestamp} - {self.national_id} - {self.is_valid}"
