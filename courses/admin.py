from django.contrib import admin
from .models import Group, Course, Lesson, Modul
from main.models import MyUser



class MyUserInline(admin.StackedInline):
    model = MyUser
    extra = 0
    fields = ('username', 'first_name', 'last_name', 'phone', 'avatar')
    show_change_link = True

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [MyUserInline]


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