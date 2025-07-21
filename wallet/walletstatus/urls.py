from .views import dashboard
from django.urls import path
urlpatterns = [
    path('', dashboard, name='dashboard'),
]