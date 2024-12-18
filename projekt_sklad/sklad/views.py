from django.shortcuts import render, get_object_or_404, redirect
from .models import Produkt, HistorieOperaci
from .forms import ProduktForm
from django.db.models import Sum, F
from django.shortcuts import render




def index(request):
    # Seskupení produktů podle názvu a ceny a součet množství
    produkty = (
        Produkt.objects
        .values('nazev', 'cena', 'popis')
        .annotate(
            celkem_mnozstvi=Sum('historieoperaci__mnozstvi'),
            posledni_uzivatel=F('historieoperaci__uzivatel__username')
        )
        .order_by('nazev', 'cena')
    )

    # Načtení historie operací
    historie = HistorieOperaci.objects.select_related('uzivatel', 'produkt')

    return render(request, 'sklad/index.html', {
        'produkty': produkty,
        'historie': historie,
    })


def detail_produktu(request, id):
    produkt = get_object_or_404(Produkt, pk=id)
    return render(request, 'sklad/detail.html', {'produkt': produkt})


def pridat_produkt(request):
    if request.method == 'POST':
        form = ProduktForm(request.POST)
        if form.is_valid():

            produkt = form.save()


            HistorieOperaci.objects.create(
                produkt=produkt,
                uzivatel=request.user,
                typ_operace='příjem',
                mnozstvi=10
            )


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
