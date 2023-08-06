from django.contrib import admin

# Register your models here.
from .models import SyncTaskObject

admin.site.register(SyncTaskObject)