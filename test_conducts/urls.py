from django.urls import path, include
from . import views

urlpatterns=[
    path('', views.tests, name='tests'),
    path('instructor/', views.instructor, name='instructor'),
]