from django.shortcuts import render, get_object_or_404, redirect
from .models import Produkt, HistorieOperaci
from .forms import ProduktForm, HistorieOperaciForm
from django.db.models import Exists, OuterRef
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages
from django.utils.dateparse import parse_datetime

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
    produkt = get_object_or_404(Produkt, id=id)
    return render(request, 'sklad/detail_produktu.html', {'produkt': produkt})

def upravit_produkt(request, produkt_id):
    produkt = get_object_or_404(Produkt, pk=produkt_id)
    if request.method == 'POST':
        form = ProduktForm(request.POST, request.FILES, instance=produkt)
        if form.is_valid():
            form.save()
            return redirect('produkty_skladem')
    else:
        form = ProduktForm(instance=produkt)
    return render(request, 'sklad/upravit_produkt.html', {'form': form, 'produkt': produkt})



def pridat_produkt(request):
    if request.method == 'POST':
        # Přidání request.FILES pro zpracování obrázků
        form = ProduktForm(request.POST, request.FILES)
        if form.is_valid():
            produkt = form.save(commit=False)
            produkt.uzivatel = request.user  # Nastavení aktuálního uživatele
            produkt.save()

            # Debugovací výstupy
            print("Ukládám produkt:", produkt.nazev)
            print("Množství produktu:", produkt.mnozstvi)
            print("Obrázek uložen na:", produkt.obrazek.url if produkt.obrazek else "Žádný obrázek nebyl nahrán.")

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
    produkty = Produkt.objects.all()

    # Inicializace aktivních filtrů
    aktivni_filtry = {}

    # Filtrování podle názvu
    nazev = request.GET.get('nazev', '').strip()
    if nazev:
        produkty = produkty.filter(nazev__icontains=nazev)
        aktivni_filtry['Název'] = nazev

    # Filtrování podle ceny
    min_cena = request.GET.get('min_cena')
    max_cena = request.GET.get('max_cena')
    if min_cena:
        produkty = produkty.filter(cena__gte=min_cena)
        aktivni_filtry['Minimální cena'] = f"{min_cena} Kč"
    if max_cena:
        produkty = produkty.filter(cena__lte=max_cena)
        aktivni_filtry['Maximální cena'] = f"{max_cena} Kč"

    # Manipulace s množstvím při POST požadavku
    if request.method == 'POST':
        produkt_id = request.POST.get('produkt_id')  # Získání ID produktu
        mnozstvi = int(request.POST.get('mnozstvi', 0))  # Získání zadaného množství
        produkt = get_object_or_404(Produkt, id=produkt_id)

        # Aktualizace množství
        produkt.mnozstvi += mnozstvi
        produkt.save()

        # Zpráva o úspěšné aktualizaci
        messages.success(request, f"Produkt {produkt.nazev} byl aktualizován. Nové množství: {produkt.mnozstvi}.")
        return redirect('produkty_skladem')

    # Předání produktů a aktivních filtrů do šablony
    return render(request, 'sklad/produkty_skladem.html', {
        'produkty': produkty,
        'aktivni_filtry': aktivni_filtry,
    })


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


    #Odebrání jednoho kusu množství z produktu a zapsání operace do historie jako výdej.
def odebrat_mnozstvi(request, produkt_id):
    # Získání produktu podle ID
    produkt = get_object_or_404(Produkt, id=produkt_id)

    # Ověření, zda lze odebrat množství
    if produkt.mnozstvi > 0:
        # Odebrání jednoho kusu
        produkt.mnozstvi -= 1
        produkt.save()

        # Získání uživatele (pokud je přihlášený)
        uzivatel = request.user if request.user.is_authenticated else None

        # Zapsání operace do historie jako výdej
        HistorieOperaci.objects.create(
            produkt=produkt,  # Odkaz na produkt
            typ_operace='výdej',  # Typ operace - Výdej
            mnozstvi=1,  # Odebrání 1 kusu
            uzivatel=uzivatel  # Pokud je přihlášený uživatel, použij ho
        )

        # Zobrazení úspěšné zprávy
        messages.success(request, f"Z produktu {produkt.nazev} byl odebrán 1 kus.")
    else:
        # Pokud je množství 0, zobrazí chybu
        messages.error(request, f"Nelze odebrat množství. Produkt {produkt.nazev} je již na nule.")

    # Přesměrování zpět na stránku s produkty
    return redirect('produkty_skladem')

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

    # Získání parametrů filtrování z GET requestu
    od_datum = request.GET.get('od_datum')  # Parametr 'od_datum' z GET
    do_datum = request.GET.get('do_datum')  # Parametr 'do_datum' z GET

    # Filtrování podle zadaných dat
    if od_datum:
        od_datum_parsed = parse_datetime(od_datum)  # Převod na datetime objekt
        if od_datum_parsed:
            historie = historie.filter(datum__gte=od_datum_parsed)  # Filtrovat záznamy po zadaném datu

    if do_datum:
        do_datum_parsed = parse_datetime(do_datum)  # Převod na datetime objekt
        if do_datum_parsed:
            historie = historie.filter(datum__lte=do_datum_parsed)  # Filtrovat záznamy do zadaného data

    # Vrátíme historii operací do šablony
    return render(request, 'sklad/historie.html', {'historie': historie})

def odebrat_produkty(request):
    if request.method == 'POST':
        action = request.POST.get("action")  # Zjištění, jaká akce byla odeslána (odebrat vybrané nebo všechny)

        if action == "delete_selected":
            produkty_ids = request.POST.getlist("produkty")  # Získání ID vybraných produktů
            produkty = Produkt.objects.filter(id__in=produkty_ids)

            # Uložení historie operace pro vybrané produkty
            for produkt in produkty:
                HistorieOperaci.objects.create(
                    produkt=produkt,
                    uzivatel=request.user,
                    typ_operace='smazání',
                    mnozstvi=produkt.mnozstvi,
                    produkt_nazev=produkt.nazev
                )

            # Smazání vybraných produktů
            produkty.delete()
            messages.success(request, f"Vybrané produkty byly úspěšně smazány.")

        elif action == "delete_all":
            produkty = Produkt.objects.all()

            # Uložení historie operace pro všechny produkty
            for produkt in produkty:
                HistorieOperaci.objects.create(
                    produkt=produkt,
                    uzivatel=request.user,
                    typ_operace='smazání',
                    mnozstvi=produkt.mnozstvi,
                    produkt_nazev=produkt.nazev
                )

            # Smazání všech produktů
            produkty.delete()
            messages.success(request, "Všechny produkty byly úspěšně smazány.")

        # Přesměrování na hlavní stránku nebo jinou dle vašeho výběru
        return redirect('index')

    # Pokud jde o GET požadavek, načteme všechny produkty pro zobrazení
    produkty = Produkt.objects.all()
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

def sledovani_zasob(request):
    # Získání všech produktů
    produkty = Produkt.objects.all()

    # Filtrace produktů, které mají nulové množství
    produkty_nedostatek = produkty.filter(mnozstvi=0)

    return render(request, 'sklad/sledovani_zasob.html', {
        'produkty': produkty,
        'produkty_nedostatek': produkty_nedostatek,
    })