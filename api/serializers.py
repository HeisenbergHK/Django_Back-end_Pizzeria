from rest_framework import serializers

from django.contrib.auth.hashers import make_password

from making_pizza.models import Pizza, Type, User, Crust, Size, Topping

# OK
class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = '__all__'

# OK
class ToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = '__all__'

# OK
class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

# OK
class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

# OK
class CrustSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crust
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'username', 'first_name', 'last_name', 'email']

class UserSerializer_noPassword(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

# class UserSerializer_POST(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
    
#     def create(self, validated_data):
#         validated_data['password'] = make_password(validated_data['password'])
#         return super().create(validated_data)
    
#     class Meta:
#         model = User
#         fields = '__all__'

class PizzaSerializer_PUT(serializers.ModelSerializer):
    # owner_username = serializers.ReadOnlyField(source='owner.username')
    # type_name = serializers.ReadOnlyField(source='type.name')
    # extra_topping_name = serializers.ReadOnlyField(source='extra_topping.name')

    # owner_username = serializers.ReadOnlyField(source='owner.username')
    # owner = UserSerializer()
    # type = TypeSerializer()
    # crust = CrustSerializer()
    # size = SizeSerializer()
    # extra_topping = ToppingSerializer(many=True, read_only=True)

    class Meta:
        model = Pizza
        # fields = ['id', 'price', 'notes', 'date_added', 'owner', 'type', 'crust', 'size', 'extra_topping']
        fields = '__all__'

class PizzaSerializer_GET(serializers.ModelSerializer):
    # owner_username = serializers.ReadOnlyField(source='owner.username')
    # type_name = serializers.ReadOnlyField(source='type.name')
    # extra_topping_name = serializers.ReadOnlyField(source='extra_topping.name')

    # owner_username = serializers.ReadOnlyField(source='owner.username')
    owner = UserSerializer_noPassword()
    type = TypeSerializer()
    crust = CrustSerializer()
    size = SizeSerializer()
    extra_topping = ToppingSerializer(many=True, read_only=True)

    class Meta:
        model = Pizza
        # fields = ['id', 'price', 'notes', 'date_added', 'owner', 'type', 'crust', 'size', 'extra_topping']
        fields = '__all__'

