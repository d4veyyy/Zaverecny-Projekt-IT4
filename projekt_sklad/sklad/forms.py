from django import forms
from .models import Produkt, HistorieOperaci

class ProduktForm(forms.ModelForm):
    class Meta:
        model = Produkt
        fields = ['nazev', 'cena', 'popis', 'mnozstvi', 'obrazek']
        widgets = {
            'nazev': forms.TextInput(attrs={'class': 'form-control'}),
            'cena': forms.NumberInput(attrs={'class': 'form-control'}),
            'popis': forms.Textarea(attrs={'class': 'form-control'}),
            'mnozstvi': forms.NumberInput(attrs={'class': 'form-control'}),
            'obrazek': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Uložíme request, abychom mohli přistupovat k uživateli
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        produkt = super().save(commit=False)
        if self.request and self.request.user:
            produkt.uzivatel = self.request.user  # Automatické přiřazení uživatele
        if commit:
            produkt.save()
        return produkt

    def save(self, commit=True):
        produkt = super().save(commit=False)
        if self.instance.pk is None:
            # Automaticky přiřadí uživatele při vytváření produktu
            produkt.uzivatel = self.initial.get('uzivatel', None)
        if commit:
            produkt.save()
        return produkt

class HistorieOperaciForm(forms.ModelForm):
    class Meta:
        model = HistorieOperaci
        fields = ['produkt', 'uzivatel', 'typ_operace', 'mnozstvi']
