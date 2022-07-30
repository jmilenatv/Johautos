from django.urls import path



from .views import (
    PageHomeView,
)


app_name = 'pages'
urlpatterns = [
    path('', PageHomeView.as_view(), name='home')
]