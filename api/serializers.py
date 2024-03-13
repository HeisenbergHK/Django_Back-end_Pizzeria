from rest_framework import serializers

from making_pizza.models import Pizza, Type, User, Crust, Size, Topping

class ToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

class CrustSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crust
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

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
        fields = ['id', 'price', 'notes', 'date_added', 'owner', 'type', 'crust', 'size', 'extra_topping']

class PizzaSerializer_GET(serializers.ModelSerializer):
    # owner_username = serializers.ReadOnlyField(source='owner.username')
    # type_name = serializers.ReadOnlyField(source='type.name')
    # extra_topping_name = serializers.ReadOnlyField(source='extra_topping.name')

    # owner_username = serializers.ReadOnlyField(source='owner.username')
    owner = UserSerializer()
    type = TypeSerializer()
    crust = CrustSerializer()
    size = SizeSerializer()
    extra_topping = ToppingSerializer(many=True, read_only=True)

    class Meta:
        model = Pizza
        fields = ['id', 'price', 'notes', 'date_added', 'owner', 'type', 'crust', 'size', 'extra_topping']

