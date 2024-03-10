from django.shortcuts import render, redirect

from .models import Pizza
from .forms import PizzaForm

def index(request):
    """This is the view of the home page"""
    return render(request, 'making_pizza/index.html')

def pizzas(request):
    """This page shows all the pizzas"""
    pizzas = Pizza.objects.order_by('date_added')
    context = {'pizzas': pizzas}
    return render(request, 'making_pizza/pizzas.html', context)

def pizza(request, pizza_id):
    """This page shows a single pizza in detail"""
    pizza = Pizza.objects.get(id=pizza_id)
    context = {'extra_topping': pizza.topping_to_string,
               'type': pizza.type,
               'crust': pizza.crust,
               'size': pizza.size,
               'notes': pizza.notes,
               'price':pizza.price}
    return render(request, 'making_pizza/pizza.html', context)


def new_pizza(request):
    """Create a new pizza"""
    if request.method != 'POST':
        # No data submitted!
        # Create a blank form
        form = PizzaForm()
    else:
        form = PizzaForm(data=request.POST)
        if form.is_valid():
            pizza = form.save(commit=False)
            pizza.price = 10
            pizza.save()
            return redirect('making_pizza:pizzas')
    
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'making_pizza/new_pizza.html', context)
