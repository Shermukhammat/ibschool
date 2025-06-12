from django.db import models
from django.utils import timezone
from solo.models import SingletonModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager 
from django.urls import reverse
from django_quill.fields import QuillField

# Create your models here.

class FAQ(models.Model):
    question = models.CharField()
    answer = models.CharField()
    created_at = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ko'p so'raladigan savol"
        verbose_name_plural = "Ko'p so'raladigan savollar"
        ordering = ('-created_at',)

    def __str__(self):
        if len(self.question) > 200:
            return self.question[:200] + '...'
        return self.question
    

class SiteSettings(SingletonModel):
    help_video_id = models.CharField(verbose_name="Yordam youtube video id", blank=True, null=True)
    help_text = models.TextField(verbose_name="Yordam teksti", blank=True, null=True)
    telegram_url = models.URLField(verbose_name="Ustoz telegrami", blank=True, null=True)


    def __str__(self):
        return "Sozlamalar"

    class Meta:
        verbose_name = "Sozlamalar"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Maqola tegi"
        verbose_name_plural = "Maqola teglari"


class PublushedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Qoralangan'),
        ('published', 'Chop etilgan'),
        ]
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique_for_date='published')
    content = QuillField()
    created = models.DateTimeField(default=timezone.now)
    published = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True)
    photo = models.ImageField(upload_to='posts/', blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, default='draft')
    short_info = models.CharField(verbose_name="qisqa tarifi", null=False, default='')
    # author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='posts', blank=True, null=True)

    class Meta:
        verbose_name = "Maqola"
        verbose_name_plural = "Maqolalar"
        ordering = ('-published',)

    objects = models.Manager()
    published_posts = PublushedManager()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post', args=[self.published.year, self.published.month, self.published.day, self.slug])
    
    
    
    def tags_list(self):
        return [tag.name for tag in self.tags.all()]
    
    def published_time(self) -> str:
        uzbek_months = {
        1: "Yanvar",
        2: "Fevral",
        3: "Mart",
        4: "Aprel",
        5: "May",
        6: "Iyun",
        7: "Iyul",
        8: "Avgust",
        9: "Sentyabr",
        10: "Oktyabr",
        11: "Noyabr",
        12: "Dekabr"
        }
        month_name = uzbek_months.get(self.published.month)
        return self.published.strftime(f"%d {month_name}, %Y, %H:%M").lstrip("0")
    
    @property
    def has_photo(self) -> bool:
        if self.photo:
            return True
        return False