from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Pizza, Type
from .forms import PizzaForm

def index(request):
    """This is the view of the home page"""
    return render(request, 'making_pizza/index.html')

def pizzas(request):
    """This page shows all the pizzas"""
    pizzas = Type.objects.all()
    context = {'pizzas': pizzas}
    return render(request, 'making_pizza/pizzas.html', context)

@login_required
def orders(request):
    """This page shows all the orders"""
    orders = Pizza.objects.order_by('-date_added').filter(owner=request.user)
    context = {'orders': orders}
    return render(request, 'making_pizza/orders.html', context)

@login_required
def order(request, order_id):
    """This page shows a single pizza in detail"""
    pizza = Pizza.objects.get(id=order_id)
    
    # Make sure the pizza belongs to the current user.
    if pizza.owner != request.user:
        raise Http404
    
    context = {'extra_topping': pizza.topping_to_string,
               'type': pizza.type,
               'crust': pizza.crust,
               'size': pizza.size,
               'notes': pizza.notes,
               'price':pizza.price}
    return render(request, 'making_pizza/order.html', context)

@login_required
def new_order(request):
    """Create a new pizza"""
    if request.method != 'POST':
        # No data submitted!
        # Create a blank form
        form = PizzaForm()
    else:
        form = PizzaForm(data=request.POST)
        if form.is_valid():
            pizza = form.save(commit=False)
            pizza.owner = request.user
            pizza = form.save()

            toppings = pizza.extra_topping.all()
            price = 0
            for top in toppings:
                price += top.cost

            pizza.price = (pizza.type.cost + pizza.crust.cost + price) * pizza.size.ratio
            pizza.save()
            return redirect('making_pizza:orders')
    
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'making_pizza/new_order.html', context)
