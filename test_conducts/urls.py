from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.tests, name='tests'),
    path('<int:s_id>/', views.s_tests, name='s_tests'),
    path('add/', views.add_test, name='add_test'),
    path('select/', views.select, name='select'),
    path('conduct/<int:test_id>/', views.conduct, name='conduct'),
    # path('instructor/', views.instructor, name='instructor'),
]
