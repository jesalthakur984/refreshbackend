from django.contrib import admin
from .models import Interest, Skill, UserProfile

# Register your models here.
admin.site.register(Interest)
admin.site.register(Skill)
admin.site.register(UserProfile)