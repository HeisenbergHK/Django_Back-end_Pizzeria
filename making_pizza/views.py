from django.shortcuts import render

def index(request):
    """This is the view of the home page"""
    return render(request, 'making_pizza/index.html')
