from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include




urlpatterns = [
	# Django APPS
	path(settings.ADMIN_URL, admin.site.urls),
	path('accounts/', include('django.contrib.auth.urls')),

	# RESTful API endpoints
    path('api/renta-autos/', include('apps.renta_autos.api.urls')),

	# Local APPS
	path('', include('apps.pages.urls', namespace='pages')),
	path('renta-autos/', include('apps.renta_autos.urls', namespace='renta_autos')),

]



if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)