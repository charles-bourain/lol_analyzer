from django.shortcuts import render
from items.utils import request_all_item_info
from django.views.generic import TemplateView
from items.models import Item

# Create your views here.
class ItemList(TemplateView):
    template_name = 'items/item_list.html'

    def get_context_data(self, **kwargs):
        context = super(ItemList, self).get_context_data(**kwargs)
        request_all_item_info()
        context['items'] = Item.objects.all()
        return context	

    def post(self, *args, **kwargs):
            get_all_champion_details()


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


