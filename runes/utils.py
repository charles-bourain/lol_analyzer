from .models import Rune
from request_manager.utils import requester

def get_static_rune_data():
    rune_url = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2/rune?api_key=07f7018c-7a66-4566-8fce-bc6f9c94b13d'

    rune_data = requester(rune_url, 'get')['data']


    for rune in rune_data:
        Rune.objects.get_or_create(
            runeId = rune_data[rune]['id'],
            name = rune_data[rune]['name'],
            description = rune_data[rune]['description']
            )





