from django.urls import path
from . import views

urlpatterns = [
    path('detect_mask', views.detect_mask, name='detect_mask'),
    path('', views.home, name='home'),
]
