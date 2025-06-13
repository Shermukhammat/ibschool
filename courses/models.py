from django.db import models

class Group(models.Model):
    name = models.CharField(verbose_name='nomi', unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Guruh"
        verbose_name_plural = "Guruhlar"

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(verbose_name='nomi', unique=True)
    slug = models.SlugField(unique=True)
    photo = models.ImageField(verbose_name="rasm", null=True, blank=True, upload_to='courses/')
    description = models.TextField(blank=True)
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

class Modul(models.Model):
    name = models.CharField(verbose_name='nomi', max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    course = models.ForeignKey(
        Course,
        null=True,
        blank=True,
        verbose_name='kurs',
        related_name='moduls',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Modul"
        verbose_name_plural = "Modullar"
        unique_together = (
            ('course', 'name'),
            ('course', 'slug'),
        )

    def __str__(self):
        return f"{self.course.name} - {self.name}"


class Lesson(models.Model):
    name = models.CharField(verbose_name='nomi', max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    modul = models.ForeignKey(
        Modul,
        verbose_name='Modul',
        related_name='lessons',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Dars"
        verbose_name_plural = "Darslar"
        unique_together = (
            ('modul', 'name'),
            ('modul', 'slug'),
        )

    def __str__(self):
        return f"{self.modul.course.name}: {self.modul.name} - {self.name}"
