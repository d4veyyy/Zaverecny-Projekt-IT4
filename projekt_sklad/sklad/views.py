from django.shortcuts import render, get_object_or_404, redirect
from .models import Produkt, HistorieOperaci
from .forms import ProduktForm, HistorieOperaciForm
from django.db.models import Exists, OuterRef
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages

@login_required
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

def upravit_produkt(request, id):
    produkt = Produkt.objects.get(id=id)
    if request.method == 'POST':
        form = ProduktForm(request.POST, instance=produkt)
        if form.is_valid():
            upravene_mnozstvi = form.cleaned_data['mnozstvi'] - produkt.mnozstvi
            produkt = form.save()

            # Záznam historie pro upravené množství
            HistorieOperaci.objects.create(
                produkt=produkt,
                uzivatel=request.user,
                typ_operace='příjem' if upravene_mnozstvi > 0 else 'výdej',
                mnozstvi=abs(upravene_mnozstvi),
                produkt_nazev=produkt.nazev
            )

            return redirect('produkty')
    else:
        form = ProduktForm(instance=produkt)

    return render(request, 'sklad/upravit_produkt.html', {'form': form, 'produkt': produkt})



def pridat_produkt(request):
    if request.method == 'POST':
        form = ProduktForm(request.POST)
        if form.is_valid():
            produkt = form.save(commit=False)
            produkt.uzivatel = request.user  # Nastavení aktuálního uživatele
            produkt.save()

            # Debugovací výstupy
            print("Ukládám produkt:", produkt.nazev)
            print("Množství produktu:", produkt.mnozstvi)

            # Automatické vytvoření historie operací
            HistorieOperaci.objects.create(
                produkt=produkt,
                uzivatel=request.user,
                typ_operace='příjem',
                mnozstvi=produkt.mnozstvi,
                produkt_nazev=produkt.nazev
            )

            print("Historie operací byla vytvořena.")

            return redirect('index')
    else:
        form = ProduktForm()
    return render(request, 'sklad/pridat_produkt.html', {'form': form})

def produkty_skladem(request):
    produkty = Produkt.objects.all()  # Získání všech produktů

    # Filtrování podle ceny
    min_cena = request.GET.get('min_cena')
    max_cena = request.GET.get('max_cena')

    if min_cena:
        produkty = produkty.filter(cena__gte=min_cena)
    if max_cena:
        produkty = produkty.filter(cena__lte=max_cena)

    if request.method == 'POST':
        produkt_id = request.POST.get('produkt_id')
        mnozstvi = int(request.POST.get('mnozstvi', 0))  # Získání zadaného množství
        produkt = get_object_or_404(Produkt, id=produkt_id)

        # Aktualizace množství
        produkt.mnozstvi += mnozstvi
        produkt.save()

        # Zpráva o úspěšné aktualizaci
        messages.success(request, f"Produkt {produkt.nazev} byl aktualizován. Nové množství: {produkt.mnozstvi}.")
        return redirect('produkty_skladem')

    return render(request, 'sklad/produkty_skladem.html', {'produkty': produkty})


def pridat_mnozstvi(request, produkt_id):
    # Získání produktu podle ID
    produkt = get_object_or_404(Produkt, id=produkt_id)

    if request.method == 'POST':
        # Zvýšení množství o 1
        produkt.mnozstvi += 1
        produkt.save()  # Uložení změny množství produktu

        # Zjištění přihlášeného uživatele, pokud je přihlášen
        uzivatel = request.user if request.user.is_authenticated else None

        # Zapsání operace do historie jako příjem
        HistorieOperaci.objects.create(
            produkt=produkt,  # Odkaz na produkt
            typ_operace='příjem',  # Typ operace - Příjem
            mnozstvi=1,  # Příjem o 1 kus
            uzivatel=uzivatel  # Pokud je přihlášený uživatel, použij ho
        )

        # Přidání zprávy o úspěchu
        messages.success(request, f'Bylo přidáno množství k produktu: {produkt.nazev}')

    # Přesměrování zpět na stránku produktů skladem
    return redirect('produkty_skladem')  # Tady se ujistíme, že jdeš zpět na správnou stránku

def smazat_produkt(request, id):
    try:
        produkt = Produkt.objects.get(id=id)
    except Produkt.DoesNotExist:
        raise Http404("Produkt nebyl nalezen")

    if request.method == 'POST':
        # Uložení historie operace před úpravou produktu
        historie = HistorieOperaci.objects.create(
            produkt=produkt,
            uzivatel=request.user,
            typ_operace='výdej',  # Změněno na "výdej"
            mnozstvi=produkt.mnozstvi,
            produkt_nazev=produkt.nazev
        )

        # Debugging: Zkontrolujte, že historie byla vytvořena
        print(f"Historie operace byla vytvořena: {historie}")

        # Nastavení množství na 0 místo smazání
        produkt.mnozstvi = 0
        produkt.save()

        # Přidání zprávy o úspěchu
        messages.success(request, f"Produkt {produkt.nazev} byl označen jako není skladem.")
        return redirect('/')

    return render(request, 'sklad/smazat_produkt.html', {'produkt': produkt})

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
        # Získání všech produktů
        produkty = Produkt.objects.all()

        # Uložení historie operace pro každý produkt
        for produkt in produkty:
            HistorieOperaci.objects.create(
                produkt=produkt,
                uzivatel=request.user,
                typ_operace='smazání',  # Pokud chcete označit jako 'smazání'
                mnozstvi=produkt.mnozstvi,
                produkt_nazev=produkt.nazev
            )

        # Smazání všech produktů
        produkty.delete()

        # Informování uživatele o úspěchu
        messages.success(request, "Všechny produkty byly úspěšně smazány.")
        return redirect('index')  # Přesměrování na hlavní stránku nebo jinou dle vašeho výběru

    produkty = Produkt.objects.all()  # Získání všech produktů pro případ, že chcete zobrazit seznam
    return render(request, 'sklad/odebrat_produkty.html', {'produkty': produkty})

def odebrat_operace(request):
    if request.method == 'POST':
        # Získání všech záznamů historie
        historie = HistorieOperaci.objects.all()

        # Uložení do historie operací před smazáním
        HistorieOperaci.objects.create(
            uzivatel=request.user,
            typ_operace='odebrání historie',
            produkt_nazev="Všechny operace",
            mnozstvi=len(historie)  # Počet smazaných operací
        )

        # Smazání všech záznamů v historii
        historie.delete()

        messages.success(request, "Všechny záznamy v historii operací byly úspěšně smazány.")
        return redirect('index')  # Přesměrování na hlavní stránku

    return render(request, 'sklad/odebrat_operace.html')