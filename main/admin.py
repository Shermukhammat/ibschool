from django.contrib import admin
from .models import FAQ, SiteSettings, Post
from solo.admin import SingletonModelAdmin
from django.utils.text import slugify


admin.site.register(FAQ)
@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', 'status')
    list_filter = ('status', 'created', 'published')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

    
    # raw_id_fields = ('author',)

    def save_model(self, request, obj, form, change):
        # Check if the title has changed or if the slug is empty
        if change and 'title' in form.changed_data:
            obj.slug = slugify(obj.title)
        elif not change:
            obj.slug = slugify(obj.title)
        super().save_model(request, obj, form, change)