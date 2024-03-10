from django import forms

from .models import Pizza

class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ['type', 'extra_topping', 'crust', 'size', 'notes']
        labels = {'type': 'Type', 'extra_topping': 'Extra Topping', 'crust': 'Crust', 'size': 'Size', 'notes': 'Notes'}
        widgets = {'notes': forms.Textarea(attrs={'cols': 80, 'rows': 4}), 
                   'extra_topping': forms.CheckboxSelectMultiple}