from django.contrib import admin
from .models import Group, Course, Lesson


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

    filter_horizontal  = ('users',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

    filter_horizontal  = ('groups',)
