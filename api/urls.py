from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('', views.index, name='index'),
    path('orders', views.get_orders, name='get_orders'),
    path('pizzas', views.get_pizzas, name='get_pizzas'),
    path('order', views.put_order, name='put_order'),
    path('test', views.test, name='test'),
    path('users', views.get_users, name='get_users'),
    path('user', views.put_user, name='put_user'),
]