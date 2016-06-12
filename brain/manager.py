from .models import *
from matches.models import Player, Match
from pybrain.structure import FeedForwardNetwork, FullConnection, LinearLayer, SigmoidLayer, RecurrentNetwork, BiasUnit, TanhLayer
from pybrain.supervised.trainers import BackpropTrainer, RPropMinusTrainer # trainer = BackpropTrainer(network, dataset)
from pybrain.datasets.supervised import SupervisedDataSet
import Queue
import pprint


"""
NetworkManager(): Wrapper for pybrain to interface with project

INPUTS:
hidden_layers: Integer - the amount of hidden layers desired
ally_champ_obj_list: List of heroes.models.Hero objects
enemy_champ_obj_list: List of heroes.models.Hero objects

METHODS:
set_nodes: builds/gets node NOTE: Temporarily builds into a dictionary.  Real version will input into DB for future calls
train_network: builds datasets and runs trainers
run_network: Runs the network as if all data is present
get_node_count: Returns the amount of inputs for the given network


"""
class NetworkManager(object):
    
    def __init__(self, hidden_layers, ally_champ_obj_list, enemy_champ_obj_list):

        self.ally_champ_obj_list = ally_champ_obj_list
        self.enemy_champ_obj_list = enemy_champ_obj_list

        self.set_nodes()

        self.network = FeedForwardNetwork()

        connect_queue = Queue.Queue()
        
        for layer in xrange(0, hidden_layers):
            connect_queue.put(TanhLayer(self.input_node_count, name = 'hidden_layer_{}'.format(layer)))

        connect_queue.put(SigmoidLayer(1, name = 'output_layer'))

        prev_layer = LinearLayer(self.input_node_count, name = 'input_layer')
        self.network.addInputModule(prev_layer)
        
        while not connect_queue.empty():
            
            current_layer = connect_queue.get()
            if current_layer.name == 'output_layer':
                self.network.addOutputModule(current_layer)
            else:
                self.network.addModule(current_layer)

            bias = BiasUnit()
            bias_connection = FullConnection(bias, current_layer, name = "bias_to_{}_connection".format(current_layer.name))
            self.network.addModule(bias)
            self.network.addConnection(bias_connection)
            
            connection = FullConnection(prev_layer, current_layer, name = "{}_to_{}_connection".format(prev_layer.name, current_layer.name))
            self.network.addConnection(connection)
            
            prev_layer = current_layer

        self.network.sortModules()

    def get_node_count(self):
        return (len(self.ally_champ_obj_list)+len(self.enemy_champ_obj_list))

    def set_nodes(self): #TEMPORARY SET_NODE - PERFORMS QUERYSET EVERYTIME - SHOULD EVENTUALLY STORE VALUES AS NODES
        node_list = {}
        match_count = 0
        champion_list = list(enumerate(self.ally_champ_obj_list + self.enemy_champ_obj_list))
        while len(champion_list) != 0:
            pid, prime = champion_list.pop()
            data = {}
            queryset = Player.objects.filter(champion = prime) 

            for (cid, champ) in champion_list:
                
                if pid <= 4 and cid <=4:
                    ally = True
                elif pid > 4 and cid > 4:
                    ally = True
                else:
                    ally = False
                
                if ally:
                    matches = queryset.filter(ally_heroes = champ)
                else:
                    matches = queryset.filter(enemy_heroes = champ)
                match_count += len(matches)

                data[champ] = {'ally':ally, 'wins':matches.filter(winner = True).count(), 'loses':matches.filter(winner = False).count()}

                node_list[prime] = data

        self.node_set = node_list
        self.input_node_count = len(champion_list)

    def train_network(self):

        training_set = SupervisedDataSet(self.input_node_count, 1)
        validation_set = SupervisedDataSet(self.input_node_count, 1)

        champion_list = list(enumerate(self.ally_champ_obj_list + self.enemy_champ_obj_list))
        while len(champion_list) != 0:
            pid, prime = champion_list.pop()
            for (cid, champ) in champion_list:

                input_set = [0]*self.input_node_count
                input_set[pid] = 1
                input_set[cid] = 1

                wins = self.node_set[prime][champ]['wins']
                loses = self.node_set[prime][champ]['loses']

                for win in xrange(0, wins):  
                    training_set.addSample(input_set, [1])
                for loss in xrange(0, loses):
                    training_set.addSample(input_set, [0])

        ally_list = self.ally_champ_obj_list
        enemy_list = self.enemy_champ_obj_list
        prime = ally_list.pop()
        validation_queryset = Player.objects.filter(champion = prime, ally_heroes__in = ally_list, enemy_heroes__in = enemy_list)
        validation_wins = validation_queryset.filter(winner = True).count()
        validation_loses = validation_queryset.filter(winner = False).count()

        for win in xrange(0, validation_wins):
            validation_set.addSample([1]*self.input_node_count, [1])
        for loss in xrange(0, validation_loses):
            validation_set.addSample([1]*self.input_node_count, [0])

        if not validation_set:
            print 'There is no Validation Set, more error in output'
        else:
            print 'Raw Win Rate = ', str(float(validation_wins)/float(validation_wins+validation_loses))    

        trainer = BackpropTrainer(self.network, learningrate = 0.5)
        trainer.trainUntilConvergence(validationData = validation_set, 
            trainingData = training_set, 
            dataset = training_set, 
            continueEpochs = 10, 
            maxEpochs = 50, 
            convergence_threshold = 1,
            )

        return  str(float(validation_wins)/float(validation_wins+validation_loses))

    def run_network(self):

        input_set = [1]*self.input_node_count
        return self.network.activate(input_set)      



"""
INPUTS:
    Inherits from NetworkManager
    pivot_data: 
        {'type': String, 
        'data': {'hero_obj': [list of objects]}} - for more complex NN, will define the information that the NN will pivot around

METHODS:

ATTRIBUTES:


"""
class PivotNetworkManager(NetworkManager):

    def __init__(self, hidden_layers, ally_champ_obj_list, enemy_champ_obj_list, pivot_data):

        self.pivot_data = pivot_data['data']
        self.pivot_type = pivot_data['type']        

        super(PivotNetworkManager, self).__init__(hidden_layers, ally_champ_obj_list, enemy_champ_obj_list)

        

    def get_node_count(self):
        if self.pivot_type == 'items':
            data_length = 7
        elif self.pivot_type == 'mastery':
            data_length = 10
        return (len(self.ally_champ_obj_list)+len(self.enemy_champ_obj_list))*(len(self.ally_champ_obj_list)+len(self.enemy_champ_obj_list)-1)*data_length

    def set_nodes(self):
        last_key = 0
        node_list = {}
        champion_list = list(enumerate(self.ally_champ_obj_list + self.enemy_champ_obj_list))
        for pid, prime in champion_list:
            node_list[prime] = {}
            for cid, champ in champion_list:
                if prime == champ:
                    continue
                if (pid <= 4 and cid <=4) or (pid > 4 and cid > 4):
                    ally = True
                    player_list = Player.objects.filter(champion = champ, ally_heroes = prime)
                else:
                    ally = False
                    player_list = Player.objects.filter(champion = champ, enemy_heroes = prime)

                node_list[prime][champ] = {'ally':ally,'data':{}}

                for key, item in enumerate(self.pivot_data[champ], start = last_key+1):
                    nodes = player_list.filter(item = item)
                    node_wins = nodes.filter(winner = True).count()
                    node_lost = nodes.filter(winner = False).count()
                    node_list[prime][champ]['data'][item] = {'wins':node_wins, 'loses':node_lost}
                    last_key = key

        self.node_set = node_list
        self.input_node_count = last_key

    def train_network(self):

        training_set = SupervisedDataSet(self.input_node_count, 1)
        validation_set = SupervisedDataSet(self.input_node_count, 1)


        next_key = 0
        for prime in self.node_set:
            for champ in self.node_set[prime]:
                for key, item in enumerate(self.pivot_data[champ], start = next_key):

                    input_set = [0]*self.input_node_count
                    input_set[key] = 1

                    wins = self.node_set[prime][champ]['data'][item]['wins']
                    loses = self.node_set[prime][champ]['data'][item]['loses']
                    next_key = key+1

                    for win in xrange(0, wins):  
                        training_set.addSample(input_set, [1])
                    for loss in xrange(0, loses):
                        training_set.addSample(input_set, [0])

        # validation_queryset = Player.objects.filter(champion = prime, ally_heroes__in = ally_list, enemy_heroes__in = enemy_list)
        # validation_wins = validation_queryset.filter(winner = True).count()
        # validation_loses = validation_queryset.filter(winner = False).count()

        # for win in xrange(0, validation_wins):
        #     validation_set.addSample([1]*self.input_node_count, [1])
        # for loss in xrange(0, validation_loses):
        #     validation_set.addSample([1]*self.input_node_count, [0])

        # if not validation_set:
        #     print 'There is no Validation Set, more error in output'
        # else:
        #     print 'Raw Win Rate = ', str(float(validation_wins)/float(validation_wins+validation_loses))    

        trainer = BackpropTrainer(self.network, learningrate = 0.5)
        trainer.trainUntilConvergence( 
            dataset = training_set, 
            continueEpochs = 10, 
            maxEpochs = 50, 
            convergence_threshold = 1,
            )




"""
BELOW HERE IS OBSOLETE
"""


#Wrapper for pybrain - does not perform any specific analysis
# class NetworkManager(object):
    
#     def __init__(self):

#         self.network = FeedForwardNetwork()

# class NetworkTrainerManager(NetworkManager):

#     def build_dataset(self, input, target):

#         data_set = SupervisedDataSet(len(self.input), len(self.target))
#         data_set.appendLinked(self.input, target)
#         self.dataset = data_set


#Broken - Data is too specific and cannot train properly.
#Plan - Set tags on Item models to group Items and build datasets based on the tags rather than specific items.
#Item tags will be tagged on similiar items - armor, magic resist, AP, AD etc etc.

#Network Layers:  Linear Input -> Tanh Hidden -> Tanh Hidden -> Sigmoid Output
#All Nodes have a Bias
#All Layers are fully connected

# MLPTrainerManager(player_object)
    #Accepts only player object - player object will contain all needed match data included enemies and allies
# class MLPTrainerManager(NetworkTrainerManager):

#     def __init__(self, player_object):

#         if not isinstance(player_object, Player):
#             raise ValueError('Object: ', player_object, ' is not a Player Object')

#         super(MLPTrainerManager, self).__init__()            

#         self.prime = player_object

#         self.ally_validator_dict= {}
#         self.enemy_validator_dict = {}

#         self.node_set_list = self.build_node_list()

#         self.input_layer = LinearLayer(len(self.node_set_list), name = 'input_layer')
#         self.hidden_layer1 = TanhLayer(len(self.node_set_list), name = 'hidden1_layer')
#         self.hidden_layer2 = TanhLayer(len(self.node_set_list), name = 'hidden2_layer')
#         self.output_layer = SigmoidLayer(1, name = 'win_layer')
#         self.bias_hidden1 = BiasUnit()
#         self.bias_hidden2 = BiasUnit()
#         self.bias_output = BiasUnit()
#         self.input_hidden1_connection = FullConnection(self.input_layer, self.hidden_layer1, name = 'input_hidden1_connection')
#         # self.hidden1_output_connection = FullConnection(self.hidden_layer1, self.output_layer, name = 'hidden1_output_connection')
#         self.hidden1_hidden2_connection = FullConnection(self.hidden_layer1, self.hidden_layer2, name = 'hidden1_hidden2_connection')
#         self.hidden2_output_connection = FullConnection(self.hidden_layer2, self.output_layer, name = 'hidden2_output_connection')
#         self.bias_hidden1_connection = FullConnection(self.bias_hidden1, self.hidden_layer1, name = 'bias_hidden1_connection')
#         self.bias_hidden2_connection = FullConnection(self.bias_hidden2, self.hidden_layer2, name = 'bias_hidden2_connection')
#         self.bias_output_connection = FullConnection(self.bias_output, self.output_layer, name = 'bias_hidden2_connection')

#         self.build_network()
#         self.train_network()


#     def build_network(self):
#         self.network.addInputModule(self.input_layer)
#         self.network.addModule(self.hidden_layer1)
#         self.network.addModule(self.hidden_layer2)      
#         self.network.addOutputModule(self.output_layer)   
#         self.network.addModule(self.bias_hidden1) 
#         self.network.addModule(self.bias_hidden2)
#         self.network.addModule(self.bias_output)            
#         self.network.addConnection(self.input_hidden1_connection)
#         self.network.addConnection(self.hidden1_hidden2_connection)
#         self.network.addConnection(self.hidden2_output_connection)
#         # self.network.addConnection(self.hidden1_output_connection)        
#         self.network.addConnection(self.bias_hidden1_connection)
#         self.network.addConnection(self.bias_hidden2_connection)
#         self.network.addConnection(self.bias_output_connection)

#         self.network.sortModules()

#     def get_node(self, prime_hero_obj, eval_hero_obj, ally_bool, item_obj):

#         if ally_bool:
#             node, created = ItemAllyNode.objects.get_or_create(prime = prime_hero_obj, ally = eval_hero_obj, item = item_obj)
#         else:
#             node, created = ItemEnemyNode.objects.get_or_create(prime = prime_hero_obj, enemy = eval_hero_obj, item = item_obj)

#         return node, created
                
#         return ally_node_list+enemy_node_list

#     def build_node_list(self):

#         ally_node_list = []
#         enemy_node_list = []

#         print '------------ %s -------------' % self.prime
        
#         for p_ally in self.prime.ally_players.all():
#             champion = p_ally.champion
#             item_set = []
#             for i in self.prime.item.all():
#                 item_set.append(i)

#                 node, created = self.get_node(self.prime.champion, champion, True, i)
                
#                 current_total = Player.objects.filter(champion = node.prime, ally_heroes = champion, item = i).count()
                
#                 #If not created, then updated with queryset of node.wins
#                 if created:
#                     ally_node_list.append(node)
#                     node.wins = Player.objects.filter(champion = node.prime, ally_heroes = champion, winner = True, item = i).count()
#                     node.total = current_total
#                     node.save()
#                 else:
#                     ally_node_list.append(node)
#                     node.total = current_total
#                     node.wins = Player.objects.filter(champion = node.prime, ally_heroes = champion, winner = True, item = i).count()
#                     # node.weight = 0.5 #TEMP -  Set up right now to re-run all matches, so needs to start from scratch.  Need an weight update function.
#                     node.save()
#             self.ally_validator_dict[champion.name] = item_set

#         for p_enemy in self.prime.enemy_players.all():
#             champion = p_enemy.champion
#             item_set = []
#             for i in p_enemy.item.all():
#                 item_set.append(i)
#                 node, created = self.get_node(self.prime.champion, champion, False, i)
                
#                 current_total = Player.objects.filter(champion = node.prime, enemy_heroes = champion, item = i).count()
                
#                 # if current_total < 10:
#                 #     continue

#                 if created:
#                     enemy_node_list.append(node)
#                     node.wins = Player.objects.filter(champion = node.prime, enemy_heroes = champion, item = i, winner = True).count()
#                     node.total = current_total
#                     node.save()
#                 else:
#                     enemy_node_list.append(node)
#                     node.total = current_total
#                     node.wins = Player.objects.filter(champion = node.prime, enemy_heroes = champion, item = i, winner = True).count()
#                     # node.weight = 0.5 #TEMP -  Set up right now to re-run all matches, so needs to start from scratch.  Need an weight update function.
#                     node.save()
#             self.enemy_validator_dict[champion] = item_set
 
#         return ally_node_list+enemy_node_list
    

#     def train_network(self):


#         lost_matches = Player.objects.filter(champion = self.prime.champion, winner = False)
#         won_matches = Player.objects.filter(champion = self.prime.champion, winner = True)

#         for hero in self.prime.ally_heroes.all():
#             lost_matches = lost_matches.filter(ally_heroes = hero)
#             won_matches = won_matches.filter(ally_heroes = hero)

#         for hero in self.prime.enemy_heroes.all():
#             lost_matches = lost_matches.filter(enemy_heroes = hero)
#             won_matches = won_matches.filter(enemy_heroes = hero)  

#         print 'Won Match Count = ', len(won_matches)
#         print 'Lost Match Count = ', len(lost_matches)          


#         training_set = SupervisedDataSet(len(self.node_set_list), 1)
#         validation_set = SupervisedDataSet(len(self.node_set_list), 1)

#         for i in xrange(0, len(self.node_set_list)):
#             node = self.node_set_list[i]
#             input_set = [0]*len(self.node_set_list)
#             input_set[i] = 1

#             j = 1
#             k = 1

#             while j <= node.wins:
#                 training_set.addSample(input_set, [1])
#                 j+=1
#             while k <= (node.total - node.wins):
#                 training_set.addSample(input_set, [0])
#                 k+=1
#         for match in won_matches:
#             valid_match = True
#             if match.winner:
#                 valid_winner = 1
#             else:
#                 valid_winner = 0

#             while valid_match:
#                 for p_ally in match.ally_players.all():
#                     print p_ally.item.all()
#                     print self.ally_validator_dict[p_ally.champion.name]
#                     if p_ally.item.all() != self.ally_validator_dict[p_ally.champion.name]:
#                         print 'Not a valid match, skipping'
#                         valid_match = False

#             if valid_match == True:
#                 validation_set.addSample([1]*len(input_set), [valid_winner])

            
#         print 'Length of Dataset = ', len(training_set)
#         print 'length of valid set = ', len(validation_set)
#         trainer = BackpropTrainer(self.network, learningrate = 0.5)

#         trainer.trainUntilConvergence(validationData = validation_set, trainingData = training_set, continueEpochs = 10, maxEpochs = 100, convergence_threshold = 1)

#     def run_network(self):

#         for i in self.prime.item.all():
#             won_matches = Player.objects.filter(champion = self.prime.champion, ally_heroes = self.prime.ally_heroes.all() , enemy_heroes = self.prime.enemy_heroes.all(), winner = True, item = i).count()
#             matches = Player.objects.filter(champion = self.prime.champion, ally_heroes = self.prime.ally_heroes.all() , enemy_heroes = self.prime.enemy_heroes.all() , item = i).count()

#         input_set = [1]*len(self.node_set_list)
#         return self.network.activate(input_set)[0], str(float(won_matches)/float(matches))


#Does not take into account any items to predict team vs team win chance
#Uses data of single hero vs single hero has training sets and validates against actual team vs. team sets
#inheritance all MLPTrainerManager.  Overwrites build_node_list function and train_network function to focus on hero vs hero
# class ChampionMLPTrainerManager(MLPTrainerManager):
    
#     def build_node_list(self):

#         ally_node_list = []
#         enemy_node_list = []
#         self.ally_validator_list = []
#         self.enemy_validator_list = []

#         print '------------ %s -------------' % self.prime
        
#         TEMP_ITEM = Item.objects.get(id = 1)

#         for p_ally in self.prime.ally_players.all():
#             champion = p_ally.champion
#             self.ally_validator_list.append(champion)
#             node, created = self.get_node(self.prime.champion, champion, True, TEMP_ITEM)
            
#             current_total = Player.objects.filter(champion = node.prime, ally_heroes = champion).count()
            
#             #If not created, then updated with queryset of node.wins
#             if created:
#                 ally_node_list.append(node)
#                 node.wins = Player.objects.filter(champion = node.prime, ally_heroes = champion, winner = True).count()
#                 node.total = current_total
#                 node.save()
#             else:
#                 ally_node_list.append(node)
#                 node.total = current_total
#                 node.wins = Player.objects.filter(champion = node.prime, ally_heroes = champion, winner = True).count()
#                 # node.weight = 0.5 #TEMP -  Set up right now to re-run all matches, so needs to start from scratch.  Need an weight update function.
#                 node.save()

#         for p_enemy in self.prime.enemy_players.all():
#             champion = p_enemy.champion
#             self.enemy_validator_list.append(champion)
#             node, created = self.get_node(self.prime.champion, champion, False, TEMP_ITEM)
            
#             current_total = Player.objects.filter(champion = node.prime, enemy_heroes = champion).count()
            
#             # if current_total < 10:
#             #     continue

#             if created:
#                 enemy_node_list.append(node)
#                 node.wins = Player.objects.filter(champion = node.prime, enemy_heroes = champion, winner = True).count()
#                 node.total = current_total
#                 node.save()
#             else:
#                 enemy_node_list.append(node)
#                 node.total = current_total
#                 node.wins = Player.objects.filter(champion = node.prime, enemy_heroes = champion, winner = True).count()
#                 # node.weight = 0.5 #TEMP -  Set up right now to re-run all matches, so needs to start from scratch.  Need an weight update function.
#                 node.save()

#         return ally_node_list+enemy_node_list

#     def train_network(self):


#         lost_matches = Player.objects.filter(champion = self.prime.champion, winner = False, ally_heroes__in = self.prime.ally_heroes.all(), enemy_heroes__in = self.prime.enemy_heroes.all()).count()
#         won_matches = Player.objects.filter(champion = self.prime.champion, winner = True, ally_heroes__in = self.prime.ally_heroes.all(), enemy_heroes__in = self.prime.enemy_heroes.all()).count()

#         print 'Won Match Count = ', won_matches
#         print 'Lost Match Count = ', lost_matches       

#         training_set = SupervisedDataSet(len(self.node_set_list), 1)
#         validation_set = SupervisedDataSet(len(self.node_set_list), 1)

#         for i in xrange(0, len(self.node_set_list)):
#             node = self.node_set_list[i]
#             input_set = [0]*len(self.node_set_list)
#             input_set[i] = 1

#             j = 1
#             k = 1

#             while j <= node.wins:
#                 training_set.addSample(input_set, [1])
#                 j+=1
#             while k <= (node.total - node.wins):
#                 training_set.addSample(input_set, [0])
#                 k+=1
#         for i in xrange(0, won_matches):
#                 validation_set.addSample([1]*len(input_set), [1])
#         for i in xrange(0,lost_matches):
#                 validation_set.addSample([1]*len(input_set), [0])

#         print 'Length of Dataset = ', len(training_set)
#         print 'length of valid set = ', len(validation_set)

#         trainer = BackpropTrainer(self.network, learningrate = 0.5)

#         trainer.trainUntilConvergence(validationData = validation_set, trainingData = training_set, continueEpochs = 10, maxEpochs = 100, convergence_threshold = 1)

#     def run_network(self):

#         lost_matches = Player.objects.filter(champion = self.prime.champion, winner = False, ally_heroes__in = self.prime.ally_heroes.all(), enemy_heroes__in = self.prime.enemy_heroes.all()).count()
#         won_matches = Player.objects.filter(champion = self.prime.champion, winner = True, ally_heroes__in = self.prime.ally_heroes.all(), enemy_heroes__in = self.prime.enemy_heroes.all()).count()

#         input_set = [1]*len(self.node_set_list)
#         return self.network.activate(input_set)[0], str(float(won_matches)/float(won_matches+lost_matches))



        
















