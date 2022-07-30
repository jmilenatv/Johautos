from django.urls import path


from .views import (
    RentaAutosClientsListSectionView,
    RentaAutosModulesSectionView,
    RentaAutoClienteEditView,
    renta_auto_cliente_delete,
    RentaAutosClientsAuditoriaListView
)


app_name = 'renta_autos'
urlpatterns = [
    path('', RentaAutosModulesSectionView.as_view(), name="renta_autos_module"),
    path('<uuid>/edit/', RentaAutoClienteEditView.as_view(), name="renta_autos_edit_cliente"),
    path('<uuid>/delete/', renta_auto_cliente_delete, name="renta_autos_delete_cliente"),
    path('cliente-lista/', RentaAutosClientsListSectionView.as_view(), name="renta_autos_clients_list"),
    path('auditoria/', RentaAutosClientsAuditoriaListView.as_view(), name="renta_autos_clients_auditoria_list"),

]