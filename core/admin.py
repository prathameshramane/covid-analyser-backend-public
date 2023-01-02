from django.contrib import admin

from .models import User, PastDisease, Report

# Register your models here.
admin.site.register(User)
admin.site.register(PastDisease)
admin.site.register(Report)
