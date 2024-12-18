from django.db import models
from django.contrib.auth.models import User

class Produkt(models.Model):
    nazev = models.CharField(max_length=200)
    popis = models.TextField(blank=True)
    cena = models.DecimalField(max_digits=10, decimal_places=2)
    mnozstvi = models.PositiveIntegerField()
    min_zasoba = models.PositiveIntegerField(default=0)


    def je_nedostatek(self):
        return self.mnozstvi >= self.min_zasoba

    def __str__(self):
        return self.nazev

class ProfilUzivatele(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefon = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('skladnik', 'Skladník')])

    def __str__(self):
        return self.user.username

from django.contrib.auth.models import User

class HistorieOperaci(models.Model):
    produkt = models.ForeignKey(Produkt, on_delete=models.CASCADE)
    uzivatel = models.ForeignKey(User, on_delete=models.CASCADE)  # Odkaz na uživatele
    datum = models.DateTimeField(auto_now_add=True)
    typ_operace = models.CharField(max_length=10, choices=[('příjem', 'Příjem'), ('výdej', 'Výdej')])
    mnozstvi = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.typ_operace} - {self.produkt.nazev} - {self.uzivatel.username if self.uzivatel else 'Nepřiřazen'}"
