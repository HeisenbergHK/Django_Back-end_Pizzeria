from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse

from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework import status

from making_pizza.models import Type, Pizza, Topping, Crust, Size, User
from .serializers import TypeSerializer, UserSerializer_GET, UserSerializer_POST, PizzaSerializer, SizeSerializer, ToppingSerializer, CrustSerializer

# Done
@api_view(['GET'])
def pizzas(request):
    if request.method != 'GET':
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        pizza_types = Type.objects.all()
        pizza_type_serialized = TypeSerializer(pizza_types, many=True)
        return Response(pizza_type_serialized.data, status=status.HTTP_200_OK)

# Done
@api_view(['GET', 'POST'])
def orders(request):
    
    try:
        orders = Pizza.objects.all()
    except Pizza.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    if request.method == 'GET':
        orders_serializer = PizzaSerializer(orders, many=True)
        return Response(orders_serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        # We store the request.data in data variable to work with it (calculating the price) then serialize it and then save it
        data = request.data
        order_serializer = PizzaSerializer(data=data)
        if order_serializer.is_valid():
            # We need to calculate the price based on the other attributes in the request

            # We calculate the topping cost
            topping_price = 0
            for i in data['extra_topping']:
                topping_price += Topping.objects.get(id=i).cost

            price = (Type.objects.get(id=data['type']).cost + Crust.objects.get(id=data['crust']).cost + topping_price) * Size.objects.get(id=data['size']).ratio
            
            price = round(price, 2)
            # Adding the price
            data['price'] = price
            order_serializer = PizzaSerializer(data=data)

            # The final save to the database with the price attribute calculated
            if order_serializer.is_valid():
                order_serializer.save()
                return Response(order_serializer.data)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# Done
@api_view(['GET', 'PUT', 'DELETE'])
def order_detail(request, order_id):
    
    try:
        order = Pizza.objects.get(id=order_id)
    except Pizza.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    if request.method == 'GET':
        order_serializer = PizzaSerializer(order)
        return Response(order_serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        order_serializer = PizzaSerializer(order, data=request.data)
        if order_serializer.is_valid():
            order_serializer.save()
            return Response(order_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    elif request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# Done
@api_view(['GET'])
def sizes(request):
    try:
        sizes = Size.objects.all()
    except Size.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    if request.method == 'GET':
        sizes_serializer = SizeSerializer(sizes, many=True)
        return Response(sizes_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# Done
@api_view(['GET'])
def size_detail(request, size_id):

    try:
        size = Size.objects.get(id=size_id)
    except Size.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    if request.method == 'GET':
        size_serializer = SizeSerializer(size)
        return Response(size_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# Done
@api_view(['GET'])
def toppings(request):
    try:
        toppings = Topping.objects.all()
    except Topping.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    if request.method == 'GET':
        toppings_serializer = ToppingSerializer(toppings, many=True)
        return Response(toppings_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# Done
@api_view(['GET'])    
def topping_detail(request, topping_id):
    try:
        topping = Topping.objects.get(id=topping_id)
    except Topping.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    if request.method == 'GET':
        topping_serializer = ToppingSerializer(topping)
        return Response(topping_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# Done
@api_view(['GET'])  
def crusts(request):
    try:
        crusts = Crust.objects.all()
    except Crust.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == 'GET':
        crusts_serializer = CrustSerializer(crusts, many=True)
        return Response(crusts_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
# Done
@api_view(['GET'])  
def crust_detail(request, crust_id):
    try:
        crust = Crust.objects.get(id=crust_id)
    except:
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    if request.method == 'GET':
        crust_serializer = CrustSerializer(crust)
        return Response(crust_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    