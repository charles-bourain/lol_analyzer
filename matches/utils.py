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
from timbad.settings import CURRENT_SEASON
import time



def get_match_list(summoner_id):
    match_list_url = 'https://na.api.pvp.net/api/lol/na/v2.2/matchlist/by-summoner/%s?seasons=%s&api_key=07f7018c-7a66-4566-8fce-bc6f9c94b13d' % (summoner_id, CURRENT_SEASON)
    try:
        match_request = requester(match_list_url,'get')
    except:
        print "Match List Request Failed"

    return match_request['matches']

def create_match_obj(match_id):
    match_url = 'https://na.api.pvp.net/api/lol/na/v2.2/match/%s?api_key=07f7018c-7a66-4566-8fce-bc6f9c94b13d' % match_id
    match_request = requester(match_url,'get')
    try:
        match, created  = Match.objects.get_or_create(match_id = match_request['matchId'])
    except:
        print 'MATCH FAILED TO CREATE, SKIPPING'





def update_league(*args):

    if args == () or args == "master":
        league_player_list_url = "https://na.api.pvp.net/api/lol/na/v2.5/league/master?type=RANKED_SOLO_5x5&api_key=07f7018c-7a66-4566-8fce-bc6f9c94b13d"
    elif args == "challenger":
        league_player_list_url = "https://na.api.pvp.net/api/lol/na/v2.5/league/challenger?type=RANKED_SOLO_5x5&api_key=07f7018c-7a66-4566-8fce-bc6f9c94b13d"
    else:
        return "League does not Exist for Search"

    try:

        league_player_list_request = requests.get(league_player_list_url).json()
    except:
            return "League Player List Request Failed"

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

def get_match_data(match_obj, current_version):

    match_id = match_obj.match_id        

    match_data_url = 'https://na.api.pvp.net/api/lol/na/v2.2/match/%s?api_key=07f7018c-7a66-4566-8fce-bc6f9c94b13d' % match_id

    match_data = requester(match_data_url, 'get')


    try:
        status_code = match_data['status']['status_code']
        status_message = match_data['status']['message']
        print 'REQUEST ERROR: %s -- %s' %(status_code, status_message)
        return False, True
    except:
        pass

    try:
        if not str(match_data['matchVersion']).startswith(str(current_version)):
            print 'Current Version = %s :: Match Version = %s'% (current_version, match_data['matchVersion'] )
            print 'Not Current Version, Skipping'
            match_obj.delete()
            return False, False
        for team in match_data['teams']:
            if team['winner'] == True:
                    winning_team = team['teamId']

        wteam = []
        lteam = []
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
                team = player['teamId'],       
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
                    try:
                        player_obj.item.add(Item.objects.get(riot_id = player['stats'][stat]))
                    except:
                        print 'Riot Item ID Failed to add: ',player['stats'][stat]

            
            if player_obj.team == winning_team:
                player_obj.winner = True
                wteam.append(player_obj)
            else:
                player_obj.winner = False
                lteam.append(player_obj)
            player_obj.save()


        for team in [wteam, lteam]:

            if team == wteam:
                ally_team = wteam
                enemy_team = lteam
            else:
                ally_team = lteam
                enemy_team = wteam

            for player in team:
                for j in ally_team:
                    if player != j:
                            player.ally_heroes.add(j.champion)
                            player.ally_players.add(j)
                    for j in enemy_team:
                        player.enemy_heroes.add(j.champion)
                        player.enemy_players.add(j)
                    player.save()

                print 'Champion = ', player.champion
                print 'Allys = ', player.ally_heroes
                print 'Enemys = ', player.enemy_heroes
                print 'Items = ', player.item
                       
        return True, True
    except:
        print 'Error Occured in Match Data for MATCH: ',match_id 
        return False, True


     



def get_all_match_data():
    current_version = requests.get('https://global.api.pvp.net/api/lol/static-data/na/v1.2/versions?api_key=07f7018c-7a66-4566-8fce-bc6f9c94b13d').json()[0]
    matches = Match.objects.all()

    for match in matches:
        if len(Player.objects.filter(match = match)) > 0: 
            print 'Match Exists, Skipping "get"'
            continue
        
        get_match_success, version_boolean  = get_match_data(match, current_version)
        
        if not get_match_success and version_boolean:
            print '-- FIRST PASS FAILED, 10 SECOND WAIT THEN SECOND ATTEMPT --'
            time.sleep(10)
            second_try_success = get_match_data(match, current_version)
            if second_try_success:
                print 'Second attempt was successful'
            else:
                print 'Second attempt unsuccessful, skipping: ', match



def get_all_static_data():
    get_static_rune_data()
    get_static_mastery_data()
    request_all_item_info()
    request_all_champion_info()
    get_all_champion_details()



def delete_matches():
    Player.objects.all().delete()
    Match.objects.all().delete()








