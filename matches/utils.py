import json
import requests
from .models import Match
from request_manager.utils import requester


def get_match_list(summoner_id):
    match_list_url = 'https://na.api.pvp.net/api/lol/na/v2.2/matchlist/by-summoner/%s?api_key=07f7018c-7a66-4566-8fce-bc6f9c94b13d' % summoner_id
    try:
        match_request = requester(match_list_url,'get')
    except:
        print "Match List Request Failed"

    return match_request['matches']


def update_matches_for_current_league_rankings(*args):
    print args
    if args == () or args == "master":
        league_player_list_url = "https://na.api.pvp.net/api/lol/na/v2.5/league/master?type=RANKED_SOLO_5x5&api_key=07f7018c-7a66-4566-8fce-bc6f9c94b13d"
    elif args == "challenger":
        league_player_list_url = "https://na.api.pvp.net/api/lol/na/v2.5/league/challenger?type=RANKED_SOLO_5x5&api_key=07f7018c-7a66-4566-8fce-bc6f9c94b13d"
    else:
        return "League does not Exist for Search"

    try:

        league_player_list_request = requests.get(league_player_list_url).json()
    except:
            "League Player List Request Failed"

    for entry in league_player_list_request['entries']:
        try:
            print "-"*10+"GETTING MATCH IDS FOR PLAYER: %r" %(entry['playerOrTeamName'])+"-"*10

            player_id = entry['playerOrTeamId']
            match_list = get_match_list(player_id)
        except:
            print "Match Request Failed"
            continue


        for i in match_list:
            match, created  = Match.objects.get_or_create(match_id = i['matchId'])
            if not created:
                pass
            else:
                match.save()















# def request_champion_details(riot_id):
#     champion = Hero.objects.get(riot_id = riot_id)
#     print champion.name, ', GOT FOR DETAILS'
#     champion_detail_url = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/%s?champData=image,info,partype,stats,tags&api_key=07f7018c-7a66-4566-8fce-bc6f9c94b13d' % riot_id
#     champion_detail_request = requests.get(champion_detail_url).json()
#     # champion.tag = str(champion_detail_request['tags'])
#     champion.attackrange = champion_detail_request['stats']['attackrange']
#     champion.mpperlevel = champion_detail_request['stats']['mpperlevel']
#     champion.mp = champion_detail_request['stats']['mp']
#     champion.attackdamage = champion_detail_request['stats']['attackdamage']
#     champion.hp = champion_detail_request['stats']['hp']
#     champion.hpperlevel = champion_detail_request['stats']['hpperlevel']
#     champion.attackdamageperlevel = champion_detail_request['stats']['attackdamageperlevel']
#     champion.armor = champion_detail_request['stats']['armor']
#     champion.mpregenperlevel = champion_detail_request['stats']['mpregenperlevel']
#     champion.hpregen = champion_detail_request['stats']['hpregen']
#     champion.critperlevel = champion_detail_request['stats']['critperlevel']
#     champion.spellblockperlevel = champion_detail_request['stats']['spellblockperlevel']
#     champion.mpregen = champion_detail_request['stats']['mpregen']
#     champion.attackspeedperlevel = champion_detail_request['stats']['attackspeedperlevel']
#     champion.spellblock = champion_detail_request['stats']['spellblock']
#     champion.movespeed = champion_detail_request['stats']['movespeed']
#     champion.attackspeedoffset = champion_detail_request['stats']['attackspeedoffset']
#     champion.crit = champion_detail_request['stats']['crit']
#     champion.hpregenperlevel = champion_detail_request['stats']['hpregenperlevel']
#     champion.armorperlevel = champion_detail_request['stats']['armorperlevel']
#     champion.save()

#     for tag in list(champion_detail_request['tags']):
#         print tag
#         champion_tag, created = HeroTag.objects.get_or_create(hero = champion, tag = tag)
#         if created == True:
#             champion_tag.save()


# def get_all_champion_details():
#     heroes = Hero.objects.all()
#     for hero in heroes:
#         try:
#             Hero.objects.get(riot_id = hero.riot_id)
#         except:
#             request_champion_details(hero.riot_id)
