from django import forms
from .models import Produkt

class ProduktForm(forms.ModelForm):
    class Meta:
        model = Produkt
        fields = ['nazev', 'popis', 'cena', 'mnozstvi', 'min_zasoba']
