from django.contrib import admin
from .models import Produkt, HistorieOperaci, ProfilUzivatele

admin.site.register(Produkt)
admin.site.register(HistorieOperaci)


class ProfilUzivateleAdmin(admin.ModelAdmin):
    list_display = ['user', 'telefon', 'role']

