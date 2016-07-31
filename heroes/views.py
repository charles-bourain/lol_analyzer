from django.shortcuts import render
from heroes.utils import request_all_champion_info, request_champion_details, get_all_champion_details
from django.views.generic import TemplateView
from heroes.models import Hero

# Create your views here.
class HeroList(TemplateView):
    template_name = 'heroes/hero_list.html'

    def get_context_data(self, **kwargs):
        request_all_champion_info()
        context = super(HeroList, self).get_context_data(**kwargs)
        context['heroes'] = Hero.objects.all()
        return context

    def post(self, *args, **kwargs):
            get_all_champion_details()


class HeroDetail(TemplateView):
    template_name = 'heroes/hero_detail.html'


    def get_context_data(self, **kwargs):
        context = super(HeroDetail, self).get_context_data(**kwargs)
        riot_id = self.kwargs['riot_id']
        request_champion_details(riot_id)
        hero = Hero.objects.get(riot_id = riot_id)
        hero_tags = HeroTag.objects.filter(hero = hero)
        print 'HERO TAGS: ', hero_tags,'FOR HERO, ', hero
        context['hero'] = hero
        return context




