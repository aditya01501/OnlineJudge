# Create your views here.
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('question/<int:question_id>', views.show_questions, name = 'question_display'),
]
