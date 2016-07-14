from matches.models import Match
from pybrain.structure import FeedForwardNetwork, FullConnection, LinearLayer, SigmoidLayer, RecurrentNetwork
from pybrain.supervised.trainers import BackpropTrainer # trainer = BackpropTrainer(network, dataset)
from pybrain.datasets.supervised import SupervisedDataSet
import time
from pprint import pprint

from .manager import PivotNetworkManager, NetworkManager

from heroes.models import Hero
from items.models import Item
from .models import DataPickler
from .manager import MLPNetwork
from copy import deepcopy, copy

def proto_data():

    node_list = {}
    champion_list = Hero.objects.all()
    for team in ['blue', 'red']:
        for champion in champion_list:
            node_list['{}-{}'.format(team, champion.name.replace("'",""))] = str(0)
    data_pickler = DataPickler.objects.create(data = node_list)
    print data_pickler.data


# def proto_network2():

#     node_list = {}

#     champion_list = Hero.objects.all()
#     item_list = Item.objects.all()
#     print item_list
#     start_with_index = 0

#     for champion in champion_list:
#         node_list[champion] = {}
#         for index, item in enumerate(item_list, start = start_with_index):
#             node_list[champion][item] = index
#         start_with_index = index + 1
#     print "Last Index = ",start_with_index-1
#     print 'length of node list = ', len(node_list)
#     network = MLPNetwork(2, data_index_size = start_with_index-1)
#     pickled_network = MLPNetworkPickler.objects.create(network = network, node_data = node_list, pivot_type = 'items')


# def network_test():
#     pickled_network = MLPNetworkPickler.objects.get(pivot_type = None)
#     network_params = pickled_network.network.params
#     print len(network_params)
    
#     #---TESTING---
#     node_list = {}
#     start_with_index = 0
#     for team in ['blue', 'red']:
#         champion_list = enumerate(Hero.objects.all().order_by('-id'), start = start_with_index)
#         node_list[team] = {}
#         for index, champion in champion_list:
#             node_list[team][champion] = index
#         start_with_index = index + 1
#     network = MLPNetwork(1, data_index_size = start_with_index).network
#     print len(network.params)
#     network._setParameters(network_params)
#     #-----TESTING---


#     highest_index_hero = Hero.objects.all().order_by('id')[0]
#     highest_index = pickled_network.node_data['red'][highest_index_hero]

#     training_set = SupervisedDataSet(highest_index+1, 1)
#     all_matches = Match.objects.all()
#     print '-- Building Datasets'
#     print '# of matches = ', len(all_matches)
#     activate_set = []
#     for match in all_matches:
#         print match
#         try:
#             dataset = [0]*(highest_index+1)
#             blue_team_heroes = []
#             red_team_heroes = []

#             for i in xrange(1,6):
#                 blue_team_heroes.append(getattr(match, 'blue_champion_{}'.format(i)))
#                 red_team_heroes.append(getattr(match, 'red_champion_{}'.format(i)))

#             for hero in blue_team_heroes:
#                 index = pickled_network.node_data['blue'][hero]
#                 #dataset[index] = 1
#                 dataset = [0]*(highest_index+1)

#             for hero in red_team_heroes:
#                 index = pickled_network.node_data['red'][hero]
#                 #dataset[index] = 1
#                 dataset = [1]*(highest_index+1)

#             if match.winning_team == 100:
#                 output_set = [1]
#             else:
#                 output_set = [0]

#             for i in xrange(1000):
#                 training_set.addSample(dataset, output_set) #Test Line
#             activate_set.append((dataset, output_set)) #Test Line
#         except:
#             print "Error in match: ", match
#     print '-- Training Network'
#     trainer = BackpropTrainer(network, learningrate = 1, verbose = True)
#     trainer.setData(training_set)
#     trainer.trainEpochs(epochs = 1000)
#     for i in activate_set:
#         print 'Predicted = ',network.activate(i[0])
#         print 'Actual = ', i[1]
#     pickled_network.network = network
#     pickled_network.save()

    


# def small_test():

#     node_list = {
#     'A':0,
#     'B':1,
#     'C':2,
#     'D':3,
#     }
#     network = MLPNetwork(2, data_index_size = 4)
#     pickled_network_obj = MLPNetworkPickler.objects.create(network = network, node_data = node_list, pivot_type = 'test') #Network Created with 2 Hidden Layers
#     network = pickled_network_obj.network.network

#     print network.activate([1,1,1,1])
    
#     zeroed_dataset = [0]*len(node_list)

#     original_params = network.params

#     training_data = [
#     [1,1,1,1],
#     [1,0,1,1],
#     [1,0,0,1],
#     [0,0,0,0],
#     [0,1,0,1],
#     [0,1,0,0],
#     ]

#     training_set = SupervisedDataSet(len(zeroed_dataset), 1)
#     trainer = BackpropTrainer(network, learningrate = .01)
    
#     for tset in training_data[:50]:
#         training_set.addSample(tset, [0])
    
#     for tset in training_data[51:]:
#         training_set.addSample(tset, [1])

#     trainer.trainUntilConvergence(
#         training_set,
#         continueEpochs = 10, 
#         maxEpochs = 50, 
#         convergence_threshold = 1,)

#     print network.activate([1,1,1,1])
#     print original_params
#     print network.params

# def test(match_id):
#     player = Player.objects.filter(match = match_id)[1]
#     MLP_NN = MLPTrainerManager(player)
#     return MLP_NN.run_network()

# def test_pivot_network():

#     match = Match.objects.get(id = 297986)
#     players = Player.objects.filter(match = match)
#     prime_player = players[0]
#     ally_team_queryset = prime_player.ally_heroes.all()
#     enemy_team_queryset = prime_player.enemy_heroes.all()
#     ally_team = map(lambda x:x, ally_team_queryset)
#     enemy_team = map(lambda x:x, enemy_team_queryset)

#     ally_team.append(prime_player.champion)

#     data = {}
#     data['type'] = 'item'
#     data['data'] = {}

#     for player in players:
#         data['data'][player.champion] = player.item.all()

#     print '--- Non-Pivot Network ---'
#     champ_network = NetworkManager(1, ally_team, enemy_team)
#     champ_network.train_network()
#     print 'Prediction = ', champ_network.run_network()
#     # print '--- Creating Network ---'
#     # network = PivotNetworkManager(1, ally_team, enemy_team, data)

#     # print '--- Training Network ---'
#     # network.train_network()

#     # print '--- Running Network ---'
#     # print 'Prediction = ', network.run_network()
#     # print 'Actual Winner = ', prime_player.winner

# def mass_test():

#     error_list = []
#     total = 0
#     wrong = 0
#     player_obj_list = Player.objects.all()
#     for player in player_obj_list:
#         MLP_NN = ChampionMLPTrainerManager(player)
#         NN_prediction, win_rate = MLP_NN.run_network()
#         if NN_prediction > 0.5:
#             win = True
#         else:
#             win = False


#         total+=1
#         print 'NN Prediction: %s -- Win Rate: %s' % (NN_prediction, win_rate)
#         if player.winner != win:
#             error_list.append((player, NN_prediction, win_rate))
#             wrong+=1
#         print "Percent Correct = ",((float(total)-float(wrong))/total)*100
#     return error_list




def delete_all_nodes():
    ItemAllyNode.objects.all().delete()
    ItemEnemyNode.objects.all().delete()


    




# def build_network(match_obj):

#     player_list = Player.objects.filter(match = match_obj)

#     ally_node_list = []
#     enemy_node_list = []


#     player = player_list[0]
#     print 'PRIME IS: ', player
#     for p_ally in player.ally_players.all():
#         champion = p_ally.champion
#         for i in player.item.all():
#             node = get_node(player.champion, champion, True, i)
#             ally_node_list.append(node)

#     for p_enemy in player.enemy_players.all():
#         champion = p_enemy.champion
#         for i in p_enemy.item.all():
#             node = get_node(player.champion, champion, False, i)
#             enemy_node_list.append(node)

#     #defining neural network
#     network = FeedForwardNetwork()
#     input_layer = LinearLayer(len(ally_node_list+enemy_node_list), name = 'item_layer')
#     output_layer = LinearLayer(1, name = 'win_layer')
#     linear_connection = FullConnection(input_layer, output_layer, name = 'c1')

#     network.addInputModule(input_layer)
#     network.addOutputModule(output_layer)

#     network.addConnection(linear_connection)

#     network.sortModules()

#     network_params = get_network_params(ally_node_list+enemy_node_list)
#     network._setParameters(network_params)

#     input_list = [1]*len(ally_node_list+enemy_node_list)
# #        weight_list.append(node.weight)

#     # input_output_connection.params = weight_list
#     return network.activate(input_list)
    


# def build_dataset(node_set_list, prime_win_bool):

#     input_set = [1]*len(node_set_list)
#     if prime_win_bool:
#         target_set = [1]
#     else:
#         target_set = [-1]

#     print 'creating dataset......'
#     data_set = SupervisedDataSet(len(input_set), len(target_set))
#     data_set.appendLinked(input_set, target_set)
#     return data_set




# def build_prime_only_network(player_obj):

#     ally_node_list = []
#     enemy_node_list = []

#     for p_ally in player_obj.ally_players.all():
#         champion = p_ally.champion
#         for i in p_ally.item.all():
#             node = get_node(player_obj.champion, champion, True, i)
#             ally_node_list.append(node)

#     for p_enemy in player_obj.enemy_players.all():
#         champion = p_enemy.champion
#         for i in p_enemy.item.all():
#             node = get_node(player_obj.champion, champion, False, i)
#             enemy_node_list.append(node)

#     #defining neural network
#     network = FeedForwardNetwork()
#     input_layer = LinearLayer(len(ally_node_list+enemy_node_list), name = 'champ/item_layer')
#     output_layer = LinearLayer(1, name = 'win_layer') # -1 to 1
#     linear_connection = FullConnection(input_layer, output_layer, name = 'c1')

#     network.addInputModule(input_layer)
#     network.addOutputModule(output_layer)

#     network.addConnection(linear_connection)

#     network.sortModules()

#     return network, ally_node_list+enemy_node_list, player_obj.winner  



# #Getting strange false items in this function.  item_obj is appear, but when Player.objects.filter is called, total = 0 in some cases.  Possible sold item?
# #Nodes built are getting more complicated (Going to Add Nodes for Masteries)
# def get_node(prime_hero_obj, eval_hero_obj, ally_bool, item_obj):

#     if ally_bool:
#         node, created = ItemAllyNode.objects.get_or_create(prime = prime_hero_obj, ally = eval_hero_obj, item = item_obj)
#     else:
#         node, created = ItemEnemyNode.objects.get_or_create(prime = prime_hero_obj, enemy = eval_hero_obj, item = item_obj)

#     total = 0
    
#     if created and ally_bool:
#         wins = Player.objects.filter(champion = prime_hero_obj, ally_heroes = eval_hero_obj, item = item_obj, winner = True).count()
#         total = Player.objects.filter(champion = prime_hero_obj, ally_heroes = eval_hero_obj, item = item_obj).count()
#     elif created and not ally_bool:
#         wins = Player.objects.filter(champion = prime_hero_obj, enemy_heroes = eval_hero_obj, item = item_obj, winner = True).count()
#         total = Player.objects.filter(champion = prime_hero_obj, enemy_heroes = eval_hero_obj, item = item_obj).count()

#     if total != 0:
#         node.save()

#     return node


# def test_build_network():
#     # ItemAllyNode.objects.all().delete()
#     # ItemEnemyNode.objects.all().delete()
#     #build_network(Match.objects.get(id = 1))
#     player = Player.objects.filter(match = Match.objects.get(id=1))[0]
#     network, node_set_list, prime_win_bool = build_prime_only_network(player)  
#     network_params = get_network_params(node_set_list)

#     network._setParameters(network_params)

#     data_set = build_dataset(node_set_list, prime_win_bool)

#     trainer = BackpropTrainer(network, data_set)
#     trainer.train()

#     new_weight_list = network.params

#     i=0
#     while i < len(node_set_list):
#         node_set_list[i].weight = network.params[i]
#         node_set_list[i].save()
#         i+=1



# def get_network_params(node_set_list):
#     param_list = []
#     for node in node_set_list:
#         param_list.append(node.weight)
#     return param_list



# def test_trained_network(id):
#     match = Match.objects.get(id = id)
#     player_set = Player.objects.filter(match = match)
#     for player in player_set:
#         print player
#         print player.winner

#     output =  build_network(match)[0]
#     percent = (output+1)/2*100

#     print 'Output = ',percent,'%'






             