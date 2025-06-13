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




# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import MyUser
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):
    """Form for creating new users with password confirmation."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    class Meta:
        model = MyUser
        fields = ('username',)

    def clean_password2(self):
        if self.cleaned_data.get("password1") != self.cleaned_data.get("password2"):
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data["password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """Form for updating users. Includes hashed password display."""
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = MyUser
        fields = ('username', 'password', 'is_active', 'is_staff', 'avatar', 'group')

@admin.register(MyUser)
class CustomUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'first_name', 'last_name', 'is_superuser', 'group')
    list_filter = ('is_staff', 'is_superuser', 'group')
    fieldsets = (
        (None,               {'fields': ('username', 'password', 'avatar', 'first_name', 'last_name', 'group')}),
        ('Permissions',      {'fields': ('is_staff','is_superuser','groups','user_permissions')}),
        ('Important dates',  {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'avatar'),
        }),
    )
    search_fields = ('username',)
    ordering = ('username',)
