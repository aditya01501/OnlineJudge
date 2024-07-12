# Create your views here.
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('contest/<int:contest_id>', views.show_contest, name = 'question_display'),
]

