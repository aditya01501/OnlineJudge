from django.contrib import admin
from django.urls import path, include
from . import views
app_name = "oj"
urlpatterns = [
    path('oj/', views.test ),
    path('oj/<int:question_id>/', views.test_oj, name = 'test_question')
]


