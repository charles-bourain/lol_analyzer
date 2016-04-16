from .models import Mastery
from request_manager.utils import requester


def get_static_mastery_data():
    mastery_url = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2/mastery?api_key=07f7018c-7a66-4566-8fce-bc6f9c94b13d'

    mastery_data = requester(mastery_url, 'get')['data']

    for mastery in mastery_data:
        Mastery.objects.get_or_create(
            masteryId = mastery_data[mastery]['id'],
            name = mastery_data[mastery]['name'],
            description = mastery_data[mastery]['description']
            )





