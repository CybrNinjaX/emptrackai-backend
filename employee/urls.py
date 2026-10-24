from django.urls import path

from .views import create_employee

urlpatterns = [
    path('', create_employee, name='create-employee'),
]
