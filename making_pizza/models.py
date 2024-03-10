from django.db import models

class Type(models.Model):
    name = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(null=True)

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
    ratio = models.FloatField()

    def __str__(self):
        return f'{self.name} with the ratio of {self.ratio}'


class Pizza(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    extra_topping = models.ManyToManyField(Topping)
    crust = models.ForeignKey(Crust, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_added = models.DateTimeField(auto_now_add=True)

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


    def __str__(self):
        return f'A {self.type.name} pizza with {self.topping_to_string()} on top.'
