from django.shortcuts import render
from heroes.utils import request_all_champion_info
from django.views.generic import TemplateView
from heroes.models import Hero

# Create your views here.
class HeroList(TemplateView):
    template_name = 'heroes/hero_list.html'

    def get_context_data(self, **kwargs):
        context = super(HeroList, self).get_context_data(**kwargs)
        request_all_champion_info()
        context['heroes'] = Hero.objects.all()
        return context




