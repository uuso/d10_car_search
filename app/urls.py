from django.urls import path
from .views import CarsList
app_name = "app"

urlpatterns = [
    path('', CarsList.as_view(), name='index'),
]
