from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pridat_produkty/', views.pridat_produkt, name='pridat_produkty'),
    path('produkt/<int:id>/', views.detail_produktu, name='detail_produktu'),
    path('upravit_produkt/<int:id>/', views.upravit_produkt, name='upravit_produkt'),
    path('pridat/', views.pridat_produkt, name='pridat'),  # Změněný název
    path('historie/', views.historie_operaci, name='historie_operaci'),
    path('produkty/', views.produkty, name='produkty'),
    path('pridat_historii/', views.pridat_historii, name='pridat_historii'),
    path('odebrat-produkty/', views.odebrat_produkty, name='odebrat_produkty'),
    path('odebrat-operace/', views.odebrat_operace, name='odebrat_operace'),
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('smazat_produkt/<int:id>/', views.smazat_produkt, name='smazat_produkt'),
    path('produkty_skladem/', views.produkty_skladem, name='produkty_skladem'),
    path('pridat_mnozstvi/<int:produkt_id>/', views.pridat_mnozstvi, name='pridat_mnozstvi'),
]

