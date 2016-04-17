import json
import requests
from .models import Match, Player
from request_manager.utils import requester
from runes.utils import get_static_rune_data
from masteries.utils import get_static_mastery_data
from items.utils import request_all_item_info
from heroes.utils import request_all_champion_info, get_all_champion_details
from runes.models import Rune
from masteries.models import Mastery
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

        mastery_rank = {}
        for mastery in player['masteries']:
            mastery_obj = Mastery.objects.get(masteryId = mastery['masteryId'])
            #player_mastery, created = PlayerMastery.objects.get_or_create(rank = mastery['rank'], mastery = mastery_obj)
            player_obj.masteries.add(mastery_obj)
            mastery_rank[mastery_obj.masteryId] = mastery['rank']

        player_obj.mastery_rank = str(mastery_rank)

        rune_rank = {}
        for rune in player['runes']:
            rune_obj = Rune.objects.get(runeId = rune['runeId'])
            #player_rune, created = PlayerRune.objects.get_or_create(rank = rune['rank'], rune = rune_obj)
            rune_rank[rune_obj.runeId] = rune['rank']
            player_obj.runes.add(rune_obj)

        player_obj.rune_rank = str(rune_rank)


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








