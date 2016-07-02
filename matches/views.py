from django.shortcuts import render
from .utils import get_all_static_data, create_match_obj
from django.views.generic import TemplateView
from .models import Match

class MatchTest(TemplateView):
    template_name = 'match/match_test.html'

    def get_context_data(self, **kwargs):
        context = super(MatchTest, self).get_context_data(**kwargs)
        test_match_id = '2094502222'
        create_match_obj('2094502222')
        #get_all_static_data()
        context['match'] = Match.objects.get(match_id = test_match_id)
        get_match_data(context['match'])

        return context  



# class HeroDetail(TemplateView):
#     template_name = 'heroes/hero_detail.html'


#     def get_context_data(self, **kwargs):
#         context = super(HeroDetail, self).get_context_data(**kwargs)
#         riot_id = self.kwargs['riot_id']
#         try:
#             hero = Hero.objects.get(riot_id = riot_id)
#         except:
#             request_champion_details(riot_id)
#             hero = Hero.objects.get(riot_id = riot_id)
#         finally:
#             context['hero'] = hero
#         return context



