from django.contrib import admin

# Register your models here.
from .models import User, InstalledApp

admin.site.register(User)
admin.site.register(InstalledApp)