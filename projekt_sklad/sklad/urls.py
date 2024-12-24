from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pridat_produkty/', views.pridat_produkt, name='pridat_produkt'),
    path('produkt/<int:id>/', views.detail_produktu, name='detail_produktu'),
    path('pridat/', views.pridat_produkt, name='pridat_produkt'),
    path('historie/', views.historie_operaci, name='historie_operaci'),
    path('produkty/', views.produkty, name='produkty'),
    path('pridat_historii/', views.pridat_historii, name='pridat_historii'),
    path('odebrat-produkty/', views.odebrat_produkty, name='odebrat_produkty'),
    path('odebrat-historii/', views.odebrat_historii, name='odebrat_historii'),
]