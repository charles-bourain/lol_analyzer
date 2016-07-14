import json
import requests
from .models import Match
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
import Queue
import csv

VERSION_TREE = ['6.13', '6.12', '6.11']


def matches_to_csv():
    schema = []
    node_index = {}
    start_with_index = 0
    for team in ['blue', 'red']:
        champion_list = enumerate(Hero.objects.all().order_by('-id'), start = start_with_index)
        node_index[team] = {}
        for index, champion in champion_list:
            node_index[team][champion] = index
            schema.append('{}-{}'.format(team,champion))
        start_with_index = index + 1

    matches = Match.objects.all()

    with open('match_data.csv', 'wb') as csv_file:
        writer = csv.writer(csv_file, delimiter = ',')
        writer.writerow([i for i in schema]+['winner'])
        for match in matches:
            indexer = [0]*len(schema)
            try:
                for i in xrange(1,6):
                    indexer[node_index['blue'][getattr(match,'blue_champion_{}'.format(i))]] = 1
                    indexer[node_index['red'][getattr(match,'red_champion_{}'.format(i))]] = 1
            except:
                print 'Error in match = ', match
                continue

            if match.winning_team == 100:
                indexer.append(1)
            else:
                indexer.append(0)
            writer.writerow(indexer)                 






    # def match_to_csv(match_obj):



def get_match_list(summoner_id):
    match_list_url = 'https://na.api.pvp.net/api/lol/na/v2.2/matchlist/by-summoner/%s?seasons=%s&api_key=07f7018c-7a66-4566-8fce-bc6f9c94b13d' % (summoner_id, CURRENT_SEASON)
    try:
        match_request = requester(match_list_url,'get')
        return match_request['matches']
    except:
        print "Match List Request Failed"
        return []
    

def create_match_obj(match_id):
    match_url = 'https://na.api.pvp.net/api/lol/na/v2.2/match/%s?api_key=07f7018c-7a66-4566-8fce-bc6f9c94b13d' % match_id
    match_request = requester(match_url,'get')
    try:
        match, created  = Match.objects.get_or_create(match_id = match_request['matchId'])
    except:
        print 'MATCH FAILED TO CREATE, SKIPPING'



def update_league(*args):

    match_request_queue = Queue.Queue()    

    def get_match_data(match_obj):
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
            if not str(match_data['matchVersion']).startswith(str(VERSION_TREE[0])) or not str(match_data['matchVersion']).startswith(str(VERSION_TREE[1])) or not str(match_data['matchVersion']).startswith(str(VERSION_TREE[2])):
                print 'Current Version = %s :: Match Version = %s'% (current_version, match_data['matchVersion'] )
                print 'Not Current Version, Skipping'
                match_obj.delete()
                return False, False
            elif match_data['queueType'] in ['RANKED_SOLO_5x5',  'RANKED_PREMADE_5x5', 'RANKED_TEAM_5x5', 'TEAM_BUILDER_DRAFT_RANKED_5x5']:
                print 'MATCH NOT RANKED'
                match_obj.delete()
                return False, False
        except:
            pass

        blue_queue = Queue.Queue()
        red_queue = Queue.Queue() 

        for i in xrange(1,6):
            blue_dict = {'champion': 'blue_champion_{}'.format(i), 'items': getattr(match_obj,'blue_items_{}'.format(i))}
            red_dict = {'champion': 'red_champion_{}'.format(i), 'items': getattr(match_obj,'red_items_{}'.format(i))}
            blue_queue.put(blue_dict)
            red_queue.put(red_dict)     
        for player in match_data['participants']:
            if player['teamId'] == 100:  # 100 is Blue team, 200 is Red Team
                match_player = blue_queue.get()
            else:
                match_player = red_queue.get()

            if player['highestAchievedSeasonTier'] in ['DIAMOND']:
                participant_id = player['participantId']

                for identity in match_data['participantIdentities']:
                    if identity['participantId'] == participant_id:
                        match_list = get_match_list(identity['player']['summonerId'])
                        for match in match_list:
                            print 'Match Added to Queue'
                            match_request_queue.put(match['matchId'])
                
            setattr(match_obj, match_player['champion'], Hero.objects.get(riot_id = player['championId']))
            for stat in player['stats']:
                if 'item' in stat and player['stats'][stat] != 0:
                    try:
                        item = Item.objects.get(riot_id = player['stats'][stat])
                        match_player['items'].add(item)
                    except:
                        print player['stats'][stat], ' No Longer exists in LoL'

        for team in match_data['teams']:
            if team['winner']:
                match_obj.winning_team = team['teamId']

        match_obj.save()


        return True, True


    league_player_list_master_url = "https://na.api.pvp.net/api/lol/na/v2.5/league/master?type=RANKED_SOLO_5x5&api_key=07f7018c-7a66-4566-8fce-bc6f9c94b13d"
    league_player_list_challenger_url = "https://na.api.pvp.net/api/lol/na/v2.5/league/challenger?type=RANKED_SOLO_5x5&api_key=07f7018c-7a66-4566-8fce-bc6f9c94b13d"
    league_player_list_requests =[]



    try:
        league_player_list_requests.append(requests.get(league_player_list_challenger_url).json())
        league_player_list_requests.append(requests.get(league_player_list_master_url).json())
    except:
            return "League Player List Request Failed"


    #Creates Root(s) for all master/challenger leagues
    for request in league_player_list_requests:
        for entry in request['entries']:
            print "-"*10+"GETTING MATCH DATA FOR PLAYER: %r" %(entry['playerOrTeamName'])+"-"*10
            player_id = entry['playerOrTeamId']
            match_list = get_match_list(player_id)
            for match in match_list:
                match_request_queue.put(match['matchId'])

    while not match_request_queue.empty():
        match_id = match_request_queue.get()
        match, created  = Match.objects.get_or_create(match_id = match_id)
        if created:
            match.save()
        print '--- Getting Match Data for {}'.format(match.match_id)
        version_match, got_data = get_match_data(match)
        if not version_match:
            continue
        if not got_data:
            version_match, second_attempt = get_match_data(match)
            if second_attempt == False:
                print 'Error getting data for Match {}'.format(match.match_id)   





def get_all_static_data():
    get_static_rune_data()
    get_static_mastery_data()
    request_all_item_info()
    request_all_champion_info()
    get_all_champion_details()



def delete_matches():
    Player.objects.all().delete()
    Match.objects.all().delete()








