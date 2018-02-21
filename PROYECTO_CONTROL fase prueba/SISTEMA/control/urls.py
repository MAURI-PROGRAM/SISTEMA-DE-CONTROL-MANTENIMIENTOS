from django.urls import path


from . import views


urlpatterns = [
    path('listar', views.dato, name='listar'),
    path('distribuir', views.mantenimientos_urg, name='distribuir'),
    path('envios.html', views.envios, name='enviosmail'),
]