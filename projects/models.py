from django.db import models

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    short_description = models.TextField(max_length=100)
    technology = models.CharField(max_length=60)
    image = models.CharField(max_length=100)

    def __str__(self):
        return self.title