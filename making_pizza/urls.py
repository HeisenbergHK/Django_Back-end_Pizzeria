# Defining URL patterns for making_pizza

from django.urls import path

from . import views

app_name = 'making_pizza'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # A page to show all the pizzas
    path('pizzas', views.pizzas, name='pizzas'),
    # New pizza
    path('new_pizza', views.new_pizza, name='new_pizza'),
]
