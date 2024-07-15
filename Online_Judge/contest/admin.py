from django.contrib import admin
from .models import Contests, Submission, Score, Leaderboard
# Register your models here.

class ContestAdmin(admin.ModelAdmin):
    list_display = ('Contest_ID', 'Name')


admin.site.register(Submission)
admin.site.register(Score)
admin.site.register(Contests, ContestAdmin)
admin.site.register(Leaderboard)