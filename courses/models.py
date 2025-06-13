from django.db import models
from main.models import MyUser

class Group(models.Model):
    name = models.CharField(verbose_name='nomi', unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(
        MyUser,
        verbose_name='foydalanuvchilar',
        related_name='course_groups',  # avoid clash with main.MyUser.groups
        related_query_name='course_group',
        blank=True,
    )

    class Meta:
        verbose_name = "Guruh"
        verbose_name_plural = "Guruhlar"

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(verbose_name='nomi', unique=True)
    slug = models.SlugField(unique=True)
    photo = models.ImageField(verbose_name="rasm", null=True, blank=True, upload_to='courses/')
    description = models.TextField()
    groups = models.ManyToManyField(
        Group,
        verbose_name='guruhlar',
        related_name='courses',
        blank=True,
    )

    class Meta:
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"

    def __str__(self):
        return self.name
    

class Lesson(models.Model):
    name = models.CharField(verbose_name='nomi', unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    course = models.ForeignKey(
        Course,
        verbose_name='kurs',
        related_name='lessons',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.course.name} - {self.name}"
