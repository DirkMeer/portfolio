from django.db import models

# Create your models here.
class Certification(models.Model):
    issuer = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=200)
    description = models.TextField()
    issue_date = models.DateField()
    technology = models.CharField(max_length=60)
    workload = models.PositiveIntegerField()
    image = models.FilePathField(path='certifications/static/img')
    url = models.URLField()

    def __str__(self):
        return self.name