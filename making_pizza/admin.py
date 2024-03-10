from django.contrib import admin

from .models import Pizza, Size, Crust, Topping, Type

admin.site.register(Pizza)
admin.site.register(Type)
admin.site.register(Topping)
admin.site.register(Crust)
admin.site.register(Size)
