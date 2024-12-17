from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pridat/', views.pridat_produkt, name='pridat_produkt'),
    path('produkt/<int:id>/', views.detail_produktu, name='detail_produktu'),
    path('pridat/', views.pridat_produkt, name='pridat_produkt'),
    path('historie/', views.historie_operaci, name='historie_operaci'),
    path('produkty/', views.produkty, name='produkty'),
]