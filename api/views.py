from rest_framework.response import Response 
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from making_pizza.models import Type, Pizza, Topping, Crust, Size, User
from .serializers import TypeSerializer, UserSerializer, PizzaSerializer, SizeSerializer, ToppingSerializer, CrustSerializer, UserSerializer_noPassword

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
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def orders(request):
    
    try:
        orders = Pizza.objects.all().filter(owner=request.user)
    except Pizza.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)
    except TypeError:
        # If the user is AnonymousUser the owner=request.user will get a TypeError
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
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

            price = data['quantity'] * ((Type.objects.get(id=data['type']).cost + Crust.objects.get(id=data['crust']).cost + topping_price) * Size.objects.get(id=data['size']).ratio)
            
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
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def order_detail(request, order_id):
    try:
        order = Pizza.objects.get(id=order_id)
        if order.owner != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Pizza.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    if request.method == 'GET':
        order_serializer = PizzaSerializer(order)
        return Response(order_serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        data = request.data
        
        # We calculate the topping cost
        topping_price = 0
        for i in data['extra_topping']:
            topping_price += Topping.objects.get(id=i).cost

        price = data['quantity'] * ((Type.objects.get(id=data['type']).cost + Crust.objects.get(id=data['crust']).cost + topping_price) * Size.objects.get(id=data['size']).ratio)
            
        price = round(price, 2)
        # Adding the price
        data['price'] = price
        order_serializer = PizzaSerializer(data=data)

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

# Done
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_detail(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # Some old users may not yet have a a token so take care of that in here
    try:
        user_token = Token.objects.get(user=request.user)
        request_token = Token.objects.get(user=user_id)
    except Token.DoesNotExist:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # We now need to check wether the user want its own info or other users
    if user_token != request_token:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == 'GET':
        user_serializer = UserSerializer_noPassword(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# Done
@api_view(['POST'])
def user_signup(request):
    if request.method == 'POST':
        user_serializer = UserSerializer_noPassword(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            # After the user has been saved to our database we can retrieve the user by the username entered by the user
            user = User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            token = Token.objects.create(user=user)
            print('data is ok')
            user.save()
            print('data is really ok!')
            user_serializer.data['password'] = ':)'
            return Response({'token': token.key, 'user': user_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(user_serializer.errors)
            # return Response(status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# Done
@api_view(['POST'])
def user_login(request):

    # Checking if the user exist
    try:
        user = User.objects.get(username=request.data['username'])
    except User.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # Checking the password
    if not user.check_password(request.data['password']):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # If the username and password is ok, then we want to get the token
    # We use get_or_create method for making sure we have a token for that user
    # Because maybe the token didn't create a the first place
    token, created = Token.objects.get_or_create(user=user)

    # Now we serialize the user to return it as a response
    user_serializer = UserSerializer_noPassword(user)
    return Response({'token': token.key, 'user': user_serializer.data}, status=status.HTTP_200_OK)

# Done
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    user = request.user
    user_serializer = UserSerializer_noPassword(user)
    return Response({'isAuthenticated': True, 'user': user_serializer.data}, status=status.HTTP_200_OK)