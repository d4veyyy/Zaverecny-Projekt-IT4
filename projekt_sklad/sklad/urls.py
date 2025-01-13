from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('pridat_produkty/', views.pridat_produkt, name='pridat_produkty'),
    path('upravit_produkt/<int:produkt_id>/', views.upravit_produkt, name='upravit_produkt'),
    path('pridat/', views.pridat_produkt, name='pridat'),  # Změněný název
    path('historie/', views.historie_operaci, name='historie_operaci'),
    path('odebrat-produkty/', views.odebrat_produkty, name='odebrat_produkty'),
    path('odebrat-operace/', views.odebrat_operace, name='odebrat_operace'),
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('smazat_produkt/<int:id>/', views.smazat_produkt, name='smazat_produkt'),
    path('produkty_skladem/', views.produkty_skladem, name='produkty_skladem'),
    path('pridat_mnozstvi/<int:produkt_id>/', views.pridat_mnozstvi, name='pridat_mnozstvi'),
    path('odebrat_mnozstvi/<int:produkt_id>/', views.odebrat_mnozstvi, name='odebrat_mnozstvi'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name="password_reset_complete"),
    path('sledovani_zasob/', views.sledovani_zasob, name='sledovani_zasob'),
    path('produkt/<int:id>/', views.detail_produktu, name='detail_produktu'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
