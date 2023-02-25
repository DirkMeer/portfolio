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
    image = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name
    

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    short_description = models.TextField(max_length=100)
    technology = models.CharField(max_length=60)
    image = models.CharField(max_length=100)

    def __str__(self):
        return self.title