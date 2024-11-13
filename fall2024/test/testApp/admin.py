from django.contrib import admin
from .models import UserProfile, Task, Project

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Task)
admin.site.register(Project)