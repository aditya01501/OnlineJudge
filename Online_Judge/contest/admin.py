from django.contrib import admin
from .models import Contests
# Register your models here.

class ContestAdmin(admin.ModelAdmin):
    list_display = ('Contest_ID', 'Name')

admin.site.register(Contests, ContestAdmin)