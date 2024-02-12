from django.urls import path
from .views import fetch_user_weight

urlpatterns = [
    path('fetch_weight/<str:user_id>/', fetch_user_weight, name='fetch_weight'),
]
