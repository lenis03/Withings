from django.urls import path
from . import views

urlpatterns = [
    path('weight/', views.weight_view, name='weight_view'),
]
