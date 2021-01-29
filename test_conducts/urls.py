from django.urls import path, include
from . import views

urlpatterns=[
    path('', views.tests, name='tests'),
    path('<int:s_id>/', views.s_tests, name='s_tests'),
    # path('instructor/', views.instructor, name='instructor'),
]