from django.urls import path


from .views import (
    ClienteRentaAutosListAPIView,
    ClienteDetailAPIView,
    RentaAutosAuditListAPIView,
)


urlpatterns = [
    path('<uuid>/', ClienteDetailAPIView.as_view(), name='cliente_detail'),
    path('list', ClienteRentaAutosListAPIView.as_view(), name='clientes_list'),
    path('auditoria/list', RentaAutosAuditListAPIView.as_view(), name='audit_list'),
]
