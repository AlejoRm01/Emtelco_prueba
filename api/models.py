from django.db import models

class Vulnerability(models.Model):
    cve_id = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    published_date = models.DateField()
    last_modified = models.DateField()
    base_severity = models.CharField(max_length=50)  
    fixed = models.BooleanField(default=False)

    def __str__(self):
        return self.cve_id