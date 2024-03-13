from django.db import models
from django.contrib.auth.models import User

class Type(models.Model):
    name = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(null=True)
    image = models.URLField()

    def __str__(self):
        return f'{self.name} with the base price of {self.cost}'

class Topping(models.Model):
    name = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(null=True)

    def __str__(self):
        return f'{self.name} with the cost of {self.cost}'

class Crust(models.Model):
    name = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(null=True)

    def __str__(self):
        return f'{self.name} with the cost of {self.cost}'

class Size(models.Model):
    name = models.CharField(max_length=200)
    ratio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.name} with the ratio of {self.ratio}'


class Pizza(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    extra_topping = models.ManyToManyField(Topping)
    crust = models.ForeignKey(Crust, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    quantity = models.IntegerField(default=1)

    date_added = models.DateTimeField(auto_now_add=True)

    def topping_to_string(self):
        topping = []
        for top in self.extra_topping.all():
            topping.append(top.name)

        if len(topping) == 1:
            topping_str = topping[0]
            return topping_str
        else:
            topping_str = ''
            for i in range(len(topping)):
                topping_str += topping[i]
                if i < len(topping)-2:
                    topping_str += ', '
                elif i < len(topping)-1:
                    topping_str += ' and '
            return topping_str
      
    def calculate_topping_price(self):
        topping = self.extra_topping.all()

        price = 0
        for top in topping:
            price += top.cost

        return price
    
    def calculate_total_price(self):
        price = (self.type.cost + self.crust.cost + self.calculate_topping_price()) * self.size.ratio
        return price
    
    def __str__(self):
        return f'A {self.type.name} pizza with {self.topping_to_string()} on top --> {self.price}'
