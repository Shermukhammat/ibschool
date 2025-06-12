from django.db import models

# Create your models here.

class Course(models.Model):
    name = models.CharField(verbose_name='nomi', unique=True, null=False, blank=False)
    slug = models.SlugField()
    description = models.TextField()

