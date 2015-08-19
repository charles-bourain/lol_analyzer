from django.conf import settings
from heroes.models import Hero
import json
import requests

def request_all_champion_info():
    all_champion_url = '/api/lol/static-data/na/v1.2/champion?api_key= %s'% settings.RIOT_API_KEY
    all_champions_request = requests.get('https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion?api_key=07f7018c-7a66-4566-8fce-bc6f9c94b13d').json()
    hero_data = all_champions_request['data']
    champion_data_list = []
   
    for item in hero_data:
        champion_data_list.append(hero_data[item])
        hero, created = Hero.objects.get_or_create(name = hero_data[item]['name'], riot_id = hero_data[item]['id'])
        if created == True:
            hero.save()