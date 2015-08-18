from django.conf import settings
import requests

def request_all_champion_info():
    all_champion_url = '/api/lol/static-data/na/v1.2/champion?api_key= %s'% settings.RIOT_API_KEY
    print all_champion_url
    all_champions = requests.get(settings.RIOT_REQUEST_BASE['NA']+all_champion_url)
    print all_champions

