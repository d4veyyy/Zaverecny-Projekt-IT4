from django.db import models
from django.contrib.auth.models import User

class Produkt(models.Model):
    nazev = models.CharField(max_length=200)
    popis = models.TextField(blank=True)
    cena = models.DecimalField(max_digits=10, decimal_places=2)
    mnozstvi = models.PositiveIntegerField()
    min_zasoba = models.PositiveIntegerField(default=0)
    uzivatel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Cizí klíč na uživatele

    def aktualizovat_stav(self):
        if self.mnozstvi > 0:
            self.stav = 'Skladem'
        else:
            self.stav = 'Není skladem'
        self.save()

    def __str__(self):
        return self.nazev

class HistorieOperaci(models.Model):
    produkt = models.ForeignKey(Produkt, on_delete=models.SET_NULL, null=True, blank=True)
    produkt_nazev = models.CharField(max_length=200, blank=True, null=True)
    uzivatel = models.ForeignKey(User, on_delete=models.CASCADE)
    datum = models.DateTimeField(auto_now_add=True)
    typ_operace = models.CharField(max_length=10, choices=[('příjem', 'Příjem'), ('výdej', 'Výdej')])
    mnozstvi = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if self.produkt and not self.produkt_nazev:
            self.produkt_nazev = self.produkt.nazev
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.typ_operace} - {self.produkt_nazev if self.produkt_nazev else 'Produkt smazán'} - {self.uzivatel.username}"
class ProfilUzivatele(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefon = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('skladnik', 'Skladník')])

    def __str__(self):
        return self.user.username



