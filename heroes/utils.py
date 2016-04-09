from django.conf import settings
from heroes.models import Hero, HeroTag
from request_manager.utils import requester
import json
import requests

def request_all_champion_info():
    all_champion_url = '/api/lol/static-data/na/v1.2/champion?api_key= %s'% settings.RIOT_API_KEY
    all_champions_request = requester('https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion?api_key=07f7018c-7a66-4566-8fce-bc6f9c94b13d','get')
    hero_data = all_champions_request['data']
    champion_data_list = []
   
    for item in hero_data:
        champion_data_list.append(hero_data[item])
        hero, created = Hero.objects.get_or_create(name = hero_data[item]['name'], riot_id = hero_data[item]['id'])
        print hero.name
        if created == True:
            hero.save()



def request_champion_details(riot_id):
    champion = Hero.objects.get(riot_id = riot_id)
    print champion.name, ', GOT FOR DETAILS'
    champion_detail_url = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/%s?champData=image,info,partype,stats,tags&api_key=07f7018c-7a66-4566-8fce-bc6f9c94b13d' % riot_id
    champion_detail_request = requester(champion_detail_url,'get')
    # champion.tag = str(champion_detail_request['tags'])
    champion.attackrange = champion_detail_request['stats']['attackrange']
    champion.mpperlevel = champion_detail_request['stats']['mpperlevel']
    champion.mp = champion_detail_request['stats']['mp']
    champion.attackdamage = champion_detail_request['stats']['attackdamage']
    champion.hp = champion_detail_request['stats']['hp']
    champion.hpperlevel = champion_detail_request['stats']['hpperlevel']
    champion.attackdamageperlevel = champion_detail_request['stats']['attackdamageperlevel']
    champion.armor = champion_detail_request['stats']['armor']
    champion.mpregenperlevel = champion_detail_request['stats']['mpregenperlevel']
    champion.hpregen = champion_detail_request['stats']['hpregen']
    champion.critperlevel = champion_detail_request['stats']['critperlevel']
    champion.spellblockperlevel = champion_detail_request['stats']['spellblockperlevel']
    champion.mpregen = champion_detail_request['stats']['mpregen']
    champion.attackspeedperlevel = champion_detail_request['stats']['attackspeedperlevel']
    champion.spellblock = champion_detail_request['stats']['spellblock']
    champion.movespeed = champion_detail_request['stats']['movespeed']
    champion.attackspeedoffset = champion_detail_request['stats']['attackspeedoffset']
    champion.crit = champion_detail_request['stats']['crit']
    champion.hpregenperlevel = champion_detail_request['stats']['hpregenperlevel']
    champion.armorperlevel = champion_detail_request['stats']['armorperlevel']
    champion.save()

    for tag in list(champion_detail_request['tags']):
        print tag
        champion_tag, created = HeroTag.objects.get_or_create(hero = champion, tag = tag)
        if created == True:
            champion_tag.save()


def get_all_champion_details():
    heroes = Hero.objects.all()
    for hero in heroes:
        try:
            Hero.objects.get(riot_id = hero.riot_id)
        except:
            request_champion_details(hero.riot_id)
