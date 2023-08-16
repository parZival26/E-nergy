from django.urls import path
from django.contrib.auth import views as auth_views
from .views import ListCasas, CreateCasas, UpdateCasas, DeleteCasas, DetailCasas, agregar_valores_view, UpdateDispositivoView, DeleteDispositivoView,AnalisisCasa, DeleteMetaView, recomendaciones_casas
from . import views


urlpatterns = [
    path('home/', ListCasas.as_view(), name='home'),
    path('home/CrearCasa/', CreateCasas.as_view(), name='crear_casa'),
    path('home/<int:pk>/update/', UpdateCasas.as_view(), name='update_casa'),
    path('home/<int:pk>/delete/', DeleteCasas.as_view(), name='delete_casa'),
    path('home/<int:pk>/detail/', DetailCasas.as_view(), name='detail_casa'),

    path('home/<int:pk>/analysis/', AnalisisCasa.as_view(), name='analisis_casa'),
    path('home/<int:pk>/recomendacion/', recomendaciones_casas.as_view(), name='recomendaciones_casa'),

    path('casa/<int:casa_id>/dispositivos/', views.ListDispositivosView.as_view(), name='list_dispositivos'),
    path('casa/<int:casa_id>/agregar-dispositivo/', views.AgregarDispositivoView.as_view(), name='agregar_dispositivo'),
    path('core/casa/<int:casa_id>/dispositivo/<int:pk>/update/', UpdateDispositivoView.as_view(), name='update_dispositivo'),
    path('core/casa/<int:casa_id>/dispositivo/<int:pk>/delete/', DeleteDispositivoView.as_view(), name='delete_dispositivo'),

    path('casa/<int:casa_id>/metas/', views.ListMetasView.as_view(), name='list_metas'),
    path('casa/<int:casa_id>/agregar-meta/', views.AgregarMetaView.as_view(), name='agregar_meta'),
    path('core/casa/<int:casa_id>/meta/<int:pk>/update/', views.UpdateMetaView.as_view(), name='update_meta'),
    path('core/casa/<int:casa_id>/meta/<int:pk>/delete/', DeleteMetaView.as_view(), name='delete_meta'),


    path('casa/<int:casa_id>/agregar-valores/', agregar_valores_view, name='agregar_valores' ),


    path('cerrar-sesion/', auth_views.LogoutView.as_view(), name='logout'),
]