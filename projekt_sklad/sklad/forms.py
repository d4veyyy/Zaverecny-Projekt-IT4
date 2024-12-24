from django import forms
from .models import Produkt, HistorieOperaci

class ProduktForm(forms.ModelForm):
    class Meta:
        model = Produkt
        fields = ['nazev', 'popis', 'cena', 'mnozstvi', 'uzivatel']  # Uživatele nebudeme vybírat, přidáme ho automaticky

    def save(self, commit=True):
        produkt = super().save(commit=False)
        if commit:
            produkt.uzivatel = self.request.user  # Nastavení uživatele při uložení
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
