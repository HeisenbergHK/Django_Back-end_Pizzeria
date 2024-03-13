from django.http import JsonResponse

from django.contrib.auth.forms import UserCreationForm

from rest_framework.response import Response 
from rest_framework.decorators import api_view

from making_pizza.models import Type, Pizza, Topping, Crust, Size, User
from .serializers import PizzaSerializer_PUT, PizzaSerializer_GET, TypeSerializer, UserSerializer_GET, UserSerializer_POST


def test(request):
    model_data = Pizza.objects.get(id=25)

    data = {'test': 'test'}

    return JsonResponse(data)


@api_view(['GET'])
def index(request):
    return JsonResponse({'message': 'This is your Django API response.'})

@api_view(['GET'])
def get_orders(request):
    # We can`t request from the terminal because we are not loged in!
    print('fuck')
    print(request.user)
    # we need to comment the .filter(owner=request.user)
    orders = Pizza.objects#.filter(owner=request.user)
    serializer = PizzaSerializer_GET(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_pizzas(request):
    pizzas = Type.objects.all()
    serializer = TypeSerializer(pizzas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer_GET(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def put_user(request):
    data = request.data
    serializer = UserSerializer_POST(data=data)

    if serializer.is_valid():
        print('new user is valid')
        serializer.save()


    return Response(serializer.data)


@api_view(['POST'])
def put_order(request):
    data = request.data
    serializer = PizzaSerializer_PUT(data=data)
    if serializer.is_valid():
            
        # Calculating the price
        topping_price = 0
        for i in data['extra_topping']:
            topping_price += Topping.objects.get(id=i).cost

        print(type(topping_price))

        price = (Type.objects.get(id=data['type']).cost + Crust.objects.get(id=data['crust']).cost + topping_price) * Size.objects.get(id=data['size']).ratio
        
        price = round(price, 2)
        # Adding the price
        data['price'] = price
        serializer = PizzaSerializer_PUT(data=data)

        if serializer.is_valid():
            serializer.save()

    return Response(serializer.data)

