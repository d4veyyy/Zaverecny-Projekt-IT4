from django.shortcuts import render, get_object_or_404, redirect
from .models import Produkt, HistorieOperaci
from .forms import ProduktForm, HistorieOperaciForm
from django.db.models import Exists, OuterRef
from django.contrib.auth.decorators import login_required
from django.db.models import Sum


def index(request):
    # Všechny produkty
    produkty = Produkt.objects.annotate(
        ma_historii=Exists(HistorieOperaci.objects.filter(produkt=OuterRef('pk')))
    )

    # Všechny historie operací
    historie = HistorieOperaci.objects.all()

    # Kontext pro předání do šablony
    kontext = {
        'produkty': produkty,
        'historie': historie,
    }

    # Vrátíme produkty a historii do šablony
    return render(request, 'sklad/index.html', kontext)



def detail_produktu(request, id):
    # Načteme produkt podle ID
    produkt = get_object_or_404(Produkt, pk=id)

    # Vrátíme detail produktu do šablony
    return render(request, 'sklad/detail.html', {'produkt': produkt})



def pridat_produkt(request):
    if request.method == 'POST':
        form = ProduktForm(request.POST)
        if form.is_valid():
            # Uložení produktu a automatické přiřazení uživatele
            produkt = form.save(commit=False)  # Neposíláme ještě do DB
            produkt.uzivatel = request.user  # Přiřazení přihlášeného uživatele
            produkt.save()  # Uložení produktu do DB

            # Vytvoření historie operace pro tento produkt
            HistorieOperaci.objects.create(
                produkt=produkt,
                uzivatel=request.user,
                typ_operace='příjem',
                mnozstvi=10
            )

            # Přesměrování na hlavní stránku
            return redirect('index')
    else:
        form = ProduktForm()  # Inicializace prázdného formuláře

    # Vrácení formuláře do šablony
    return render(request, 'sklad/pridat_produkt.html', {'form': form})


def historie_operaci(request):
    # Načteme všechny operace z historie
    historie = HistorieOperaci.objects.all()

    # Vrátíme historii operací do šablony
    return render(request, 'sklad/historie.html', {'historie': historie})


def produkty(request):
    # Načteme všechny produkty z databáze
    produkty = Produkt.objects.all()

    # Vrátíme produkty do šablony
    return render(request, 'sklad/produkty.html', {'produkty': produkty})


@login_required
def pridat_produkt(request):
    if request.method == 'POST':
        form = ProduktForm(request.POST)
        if form.is_valid():
            produkt = form.save(commit=False)
            produkt.uzivatel = request.user  # Přiřazení přihlášeného uživatele
            produkt.save()
            return redirect('produkty')  # Přesměrování na seznam produktů
    else:
        form = ProduktForm()
    return render(request, 'sklad/pridat_produkt.html', {'form': form})
def pridat_historii(request):
    if request.method == 'POST':
        form = HistorieOperaciForm(request.POST)
        if form.is_valid():
            form.save()  # Uložení historie operace
            return redirect('index')  # Přesměrování zpět na hlavní stránku
    else:
        form = HistorieOperaciForm()  # Inicializace formuláře pro historii operací

    # Vrácení formuláře do šablony
    return render(request, 'sklad/pridat_historii.html', {'form': form})

def odebrat_produkty(request):
    if request.method == 'POST':
        produkt_id = request.POST.get('produkt_id')
        produkt = get_object_or_404(Produkt, id=produkt_id)
        produkt.delete()  # Smazání produktu
        return redirect('index')  # Přesměrování na hlavní stránku

    produkty = Produkt.objects.all()  # Získání všech produktů
    return render(request, 'sklad/odebrat_produkt.html', {'produkty': produkty})

def odebrat_historii(request):
    if request.method == 'POST':
        historie_id = request.POST.get('historie_id')
        operace = get_object_or_404(HistorieOperaci, id=historie_id)
        operace.delete()  # Smazání vybrané historie operace
        return redirect('index')  # Přesměrování na hlavní stránku

    historie = HistorieOperaci.objects.all()  # Načtení všech záznamů historie
    return render(request, 'sklad/odebrat_historii.html', {'historie': historie})