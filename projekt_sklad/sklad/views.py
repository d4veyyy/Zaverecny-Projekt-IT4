from django.shortcuts import render, get_object_or_404, redirect
from .models import Produkt, HistorieOperaci
from .forms import ProduktForm

def index(request):
    produkty = Produkt.objects.all()
    return render(request, 'sklad/index.html', {'produkty': produkty})

def detail_produktu(request, id):
    produkt = get_object_or_404(Produkt, pk=id)
    return render(request, 'sklad/detail.html', {'produkt': produkt})

def pridat_produkt(request):
    if request.method == 'POST':
        form = ProduktForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProduktForm()
    return render(request, 'sklad/pridat_produkt.html', {'form': form})

def historie_operaci(request):
    historie = HistorieOperaci.objects.all().order_by('-datum')
    return render(request, 'sklad/historie.html', {'historie': historie})

def produkty(request):
    # Načteme všechny produkty z databáze
    produkty = Produkt.objects.all()  # Předpokládáme, že máte model Produkt
    return render(request, 'sklad/produkty.html', {'produkty': produkty})

def pridat_produkt(request):
    form = ProduktForm()  # Inicializace formuláře

    if request.method == 'POST':
        form = ProduktForm(request.POST)  # Přijetí dat formuláře
        if form.is_valid():
            # Zpracování formuláře a uložení
            form.save()
            return redirect('produkty')  # Přesměrování na seznam produktů

    # Vždy předávejte form do šablony
    return render(request, 'sklad/pridat_produkt.html', {'form': form})
