from django.db import models
from django.utils import timezone
from django.urls import reverse
from django_quill.fields import QuillField

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
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"

    def __str__(self):
        return self.name

    def short_description(self) -> str:
        if self.description:
            if len(self.description) < 100:
                return self.description
            else:
                return self.description[:95] + '...'
        return ''
    
    def lessons_leng(self):
        return Lesson.objects.filter(modul__course=self).count()

    def modules_leng(self):
        return self.moduls.count()

class Modul(models.Model):
    name = models.CharField(verbose_name='nomi', max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=False)
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
    name        = models.CharField(verbose_name='nomi',   max_length=255)
    slug        = models.SlugField(max_length=255)
    description = QuillField(verbose_name='Dars kontenti')
    modul       = models.ForeignKey(
        'Modul',
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
        ordering = ['modul__pk', 'pk']

    def __str__(self):
        return f"{self.modul.course.name}: {self.modul.name} - {self.name}"

    def abs_url(self):
        return f"/courses/{self.modul.course.slug}/{self.modul.slug}/{self.slug}"
    
    def course_url(self):
        return f"/courses/{self.modul.course.slug}"

    def get_next_lesson(self):
        """
        Returns the next Lesson instance in the course sequence.
        Checks within the same module first, then the first lesson of the next module.
        """
        # 1) Next in current module
        next_in_modul = Lesson.objects.filter(
            modul=self.modul,
            pk__gt=self.pk
        ).order_by('pk').first()
        if next_in_modul:
            return next_in_modul

        # 2) First lesson of the next module
        next_modul = Modul.objects.filter(
            course=self.modul.course,
            pk__gt=self.modul.pk
        ).order_by('pk').first()
        if next_modul:
            return Lesson.objects.filter(
                modul=next_modul
            ).order_by('pk').first()

        return None

    def get_previous_lesson(self):
        """
        Returns the previous Lesson instance in the course sequence.
        Checks within the same module first, then the last lesson of the previous module.
        """
        # 1) Previous in current module
        prev_in_modul = Lesson.objects.filter(
            modul=self.modul,
            pk__lt=self.pk
        ).order_by('-pk').first()
        if prev_in_modul:
            return prev_in_modul

        # 2) Last lesson of the previous module
        prev_modul = Modul.objects.filter(
            course=self.modul.course,
            pk__lt=self.modul.pk
        ).order_by('-pk').first()
        if prev_modul:
            return Lesson.objects.filter(
                modul=prev_modul
            ).order_by('-pk').first()

        return None

    def get_next_url(self) -> str:
        """
        Returns the URL of the next lesson in sequence, or None.
        """
        nxt = self.get_next_lesson()
        return nxt.abs_url() if nxt else None

    def get_previous_url(self) -> str:
        """
        Returns the URL of the previous lesson in sequence, or None.
        """
        prev = self.get_previous_lesson()
        return prev.abs_url() if prev else None
