from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin




class PageHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/home.html'
