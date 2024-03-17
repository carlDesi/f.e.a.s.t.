from django.contrib import admin
from django.urls import path, include
from . import views
from .views import teacher_main

urlpatterns = [
    path('login/', views.loginpage, name="loginpage"), #'endpoint' views.function_name, 
    path('signup/', views.signup, name='signup'),
    path('loginerror/', views.loginerror, name='loginerror'),
    path('student_main/', views.student_main, name='student_main'),
    path('teacher_main/', teacher_main, name="teacher_main"),
    path('teacher_main/create_room/', teacher_main, name='create_room'),
]