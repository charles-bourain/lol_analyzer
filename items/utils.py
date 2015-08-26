from django.conf import settings
from items.models import Item
import json
import requests

def request_all_item_info():
    all_item_request = requests.get('https://global.api.pvp.net/api/lol/static-data/na/v1.2/item?locale=en_US&itemListData=all&api_key=07f7018c-7a66-4566-8fce-bc6f9c94b13d').json()
    item_data = all_item_request['data']
    item_data_list = []
   
    for item in item_data:
        print item_data[item]['name']
        item_data_list.append(item_data[item])
        item, created = Item.objects.get_or_create(name = item_data[item]['name'], riot_id = item_data[item]['id'])
        if created == True:
            item.save()    

# def get_all_champion_details():
#     heroes = Hero.objects.all()
#     for hero in heroes:
#         try:
#             Hero.objects.get(riot_id = hero.riot_id)
#         except:
#             request_champion_details(hero.riot_id)
