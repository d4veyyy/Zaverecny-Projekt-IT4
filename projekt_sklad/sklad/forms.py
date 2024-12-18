from django import forms
from .models import Produkt

class ProduktForm(forms.ModelForm):
    mnozstvi = forms.IntegerField(
        label="Množství",
        min_value=1,  # Minimální množství
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Produkt
        fields = ['nazev', 'popis', 'cena', 'mnozstvi']  # Přidejte další pole modelu, pokud je to potřeba
