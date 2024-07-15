# Create your views here.
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('contest/<int:contest_id>', views.show_contest, name = 'question_display'),
    path('Leaderboard/<int:contest_id>', views.show_leaderboard, name = 'leaderboard'),
    path('contest/register', views.register_contest, name = 'register_contest'),
    path('contest/<int:contest_id>/<int:question_id>', views.contest_qna, name = 'contest_question'),
    path('contest/getlbrd/<int:contest_id>', views.get_leaderboard, name = 'get_leaderboard')
]

