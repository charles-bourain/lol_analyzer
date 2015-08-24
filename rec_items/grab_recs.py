from heroes.models import Hero
import requests
import BeautifulSoup
from django.template.defaultfilters import slugify


def grab_items():
    heroes = Hero.objects.all()

    for hero in heroes:
        name = hero.name
        url = "http://www.lolcounter.com/champions/" + slugify(name)
        req = requests.get(url)
        raw = req.text
        poop = BeautifulSoup(raw, 'html.parser')
        divs = poop.find_all(class="summoners")
        print divs