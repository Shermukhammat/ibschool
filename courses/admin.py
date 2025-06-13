from django.contrib import admin
from .models import Group, Course, Lesson, Modul



@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

    # filter_horizontal  = ('users',)


class ModulInline(admin.TabularInline):
    model = Modul
    extra = 0
    show_change_link = True 
    prepopulated_fields = {'slug':('name',)}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

    filter_horizontal  = ('groups',)
    inlines = [ModulInline]



class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    show_change_link = True
    prepopulated_fields = {'slug':('name',)}

@admin.register(Modul)
class ModulAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

    inlines = [LessonInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}