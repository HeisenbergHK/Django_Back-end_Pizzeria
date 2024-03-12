
from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('', views.get_data_test, name='get_data_test'),
]