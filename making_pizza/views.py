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


def new_pizza(request):
    """Create a new pizza"""
    if request.method != 'POST':
        # No data submitted!
        # Create a blank form
        form = PizzaForm()
    else:
        form = PizzaForm(data=request.POST)
        form.price = 10
        if form.is_valid():
            form.save()
            return redirect('making_pizza:index')
    
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'making_pizza/new_pizza.html', context)
