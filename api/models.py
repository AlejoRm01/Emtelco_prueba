from django.db import models

# Create your models here.
class Vulnerability(models.Model):
    cve_id = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    severity = models.CharField(max_length=20)  # e.g., Low, Medium, High, Critical
    fixed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.cve_id