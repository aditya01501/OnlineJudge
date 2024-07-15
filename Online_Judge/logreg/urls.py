from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.Login ),
    path('register', views.register),
    path('logout', views.Logout),
    path('ProfilePage', views.Profile),

]
