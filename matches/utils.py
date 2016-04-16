import json
import requests
from .models import Match, Player
from request_manager.utils import requester
from runes.utils import get_static_rune_data
from masteries.utils import get_static_mastery_data
from items.utils import request_all_item_info
from heroes.utils import request_all_champion_info, get_all_champion_details
from runes.models import Rune, PlayerRune
from masteries.models import Mastery, PlayerMastery
from items.models import Item
from heroes.models import Hero


def get_match_list(summoner_id):
    match_list_url = 'https://na.api.pvp.net/api/lol/na/v2.2/matchlist/by-summoner/%s?api_key=07f7018c-7a66-4566-8fce-bc6f9c94b13d' % summoner_id
    try:
        match_request = requester(match_list_url,'get')
    except:
        print "Match List Request Failed"

    return match_request['matches']

def create_match_obj(match_id):
    match_url = 'https://na.api.pvp.net/api/lol/na/v2.2/match/%s?api_key=07f7018c-7a66-4566-8fce-bc6f9c94b13d' % match_id
    match_request = requester(match_url,'get')
    match, created  = Match.objects.get_or_create(match_id = match_request['matchId'])





def update_matches_for_current_league_rankings(*args):
    match_count = 0   #TEMP TO CONTROL MATCH_ROW LIMIT

    while match_count <= 5000: #TEMP TO CONTROL MATCH_ROW LIMIT
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
                match_count += 1   #TEMP TO CONTROL MATCH_ROW LIMIT
                match, created  = Match.objects.get_or_create(match_id = i['matchId'])
                if not created:
                    pass
                else:
                    match.save()

def get_match_data(match_obj):

    match_id = match_obj.match_id        

    match_data_url = 'https://na.api.pvp.net/api/lol/na/v2.2/match/%s?api_key=07f7018c-7a66-4566-8fce-bc6f9c94b13d' % match_id

    match_data = requester(match_data_url, 'get')
    
    for team in match_data['teams']:
        if team['winner'] == True:
            winning_team = team['teamId']

    for player in match_data['participants']:

        (player_obj, created) = Player.objects.get_or_create(
            match = match_obj, 
            json_response = player,
            champion = Hero.objects.get(riot_id = player['championId']),
            spell1 = player['spell1Id'],
            spell2 = player['spell2Id'],
            totalDamageTaken = player['stats']['totalDamageTaken'],
            physicalDamageTaken = player['stats']['physicalDamageTaken'],
            magicDamageTaken = player['stats']['magicDamageTaken'],
            sightWardsBoughtInGame = player['stats']['sightWardsBoughtInGame'],
            visionWardsBoughtInGame = player['stats']['visionWardsBoughtInGame'],
            wardsKilled = player['stats']['wardsKilled'],
            wardsPlaced = player['stats']['wardsPlaced'],
            deaths = player['stats']['deaths'],
            assists = player['stats']['assists'],
            kills = player['stats']['kills'],
            firstBloodAssist = player['stats']['firstBloodAssist'],
            magicDamageDealtToChampions = player['stats']['magicDamageDealtToChampions'],
            physicalDamageDealtToChampions = player['stats']['physicalDamageDealtToChampions'],
            totalDamageDealtToChampions = player['stats']['totalDamageDealtToChampions'],
            totalTimeCrowdControlDealt = player['stats']['totalTimeCrowdControlDealt'],
            minionsKilled = player['stats']['minionsKilled'],
            goldEarned = player['stats']['goldEarned'],
            totalHeal = player['stats']['totalHeal'],         
            )

        for mastery in player['masteries']:
            mastery_obj = Mastery.objects.get(masteryId = mastery['masteryId'])
            player_mastery, created = PlayerMastery.objects.get_or_create(rank = mastery['rank'], mastery = mastery_obj)
            player_obj.masteries.add(player_mastery)

        for rune in player['runes']:
            rune_obj = Rune.objects.get(runeId = rune['runeId'])
            player_rune, created = PlayerRune.objects.get_or_create(rank = rune['rank'], rune = rune_obj)
            player_obj.runes.add(player_rune)

        for stat in player['stats']:
            if 'item' in stat and player['stats'][stat] != 0:
                player_obj.item.add(Item.objects.get(riot_id = player['stats'][stat]))

        
        if player_obj.team and winning_team == 200:
            player_obj.winner = True
        elif not player_obj.team and winning_team == 100:
            player_obj.winner = True
        else:
            player_obj.winner = False
        player_obj.save()





def get_all_match_data():
    matches = Match.objects.all()

    for match in matches:
        if len(Player.objects.filter(match = match)) > 0: 
            print 'Match Exists, Skipping "get"'
        else:
            get_match_data(match)





def get_all_static_data():
    get_static_rune_data()
    get_static_mastery_data()
    request_all_item_info()
    request_all_champion_info()
    get_all_champion_details()





def delete_matches():
    Player.objects.all().delete()
    Match.objects.all().delete()









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
