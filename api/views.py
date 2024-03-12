# from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.decorators import api_view


from making_pizza.models import Type


@api_view(['GET'])
def get_data(request):
    pizza_types = Type.objects.all()

@api_view(['GET'])
def get_data_test(request):
    data = {'pizza': 'test_pizza',
            'topping': 'test_topping'}
    return Response(data)

