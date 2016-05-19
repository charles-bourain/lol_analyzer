from .models import *
from matches.models import Player, Match
from pybrain.structure import FeedForwardNetwork, FullConnection, LinearLayer, SigmoidLayer, RecurrentNetwork, BiasUnit
from pybrain.supervised.trainers import BackpropTrainer # trainer = BackpropTrainer(network, dataset)
from pybrain.datasets.supervised import SupervisedDataSet


class NetworkManager(object):
    
    def __init__(self):

        self.network = FeedForwardNetwork()

    def build_network(self):

        try:
            self.network.addInputModule(self.input_layer)    
            self.network.addOutputModule(self.output_layer)               
            self.network.addConnection(self.linear_connection)
            self.network.sortModules()
            self.replace_network_parms_with_node_values()
        except(NameError):
            pass

    def replace_network_parms_with_node_values(self):
        param_list = []
        for node in self.node_set_list:
            param_list.append(node.weight)
        self.network._setParameters(param_list)

    


class NetworkTrainerManager(NetworkManager):

    def build_dataset(self, input, target):

        data_set = SupervisedDataSet(len(self.input), len(self.target))
        data_set.appendLinked(self.input, target)
        self.dataset = data_set

    def train(self, network, dataset, node_set):

        if not isinstance(node_set, list):
            node_set = [node_set]

        trainer = BackpropTrainer(network, dataset)

        trainer.train()

        new_weight_list = network.params

        i=0
        while i < len(node_set):
            node_set[i].weight = network.params[i]
            node_set[i].save()
            i+=1




# class PrimeTrainingNetworkManager(NetworkTrainerManager):

#     def __init__(self, player_object):

#         if not isinstance(player_object, Player):
#             raise ValueError('Object: ', player_object, ' is not a Player Object')

#         super(PrimeTrainingNetworkManager, self).__init__()            

#         self.prime = player_object

#         ally_node_list = []
#         enemy_node_list = []

#         for p_ally in self.prime.ally_players.all():
#             champion = p_ally.champion
#             for i in self.prime.item.all():
#                 node = self.get_node(self.prime.champion, champion, True, i)
#                 ally_node_list.append(node)

#         for p_enemy in self.prime.enemy_players.all():
#             champion = p_enemy.champion
#             for i in p_enemy.item.all():
#                 node = self.get_node(self.prime.champion, champion, False, i)
#                 enemy_node_list.append(node)        

#         self.input_layer = LinearLayer(len(ally_node_list+enemy_node_list), name = 'item_layer')
#         self.input = [1]*len(ally_node_list+enemy_node_list)
#         self.output_layer = LinearLayer(1, name = 'win_layer')
#         self.linear_connection = FullConnection(self.input_layer, self.output_layer, name = 'c1')

#         if self.prime.winner:
#             self.target = [1]
#         else:
#             self.target = [0]
        
#         self.node_set_list = ally_node_list+enemy_node_list

#         self.build_network()


#     def get_node(self, prime_hero_obj, eval_hero_obj, ally_bool, item_obj):

#         if ally_bool:
#             node, created = ItemAllyNode.objects.get_or_create(prime = prime_hero_obj, ally = eval_hero_obj, item = item_obj)
#         else:
#             node, created = ItemEnemyNode.objects.get_or_create(prime = prime_hero_obj, enemy = eval_hero_obj, item = item_obj)

#         total = 0
        
#         if created and ally_bool:
#             wins = Player.objects.filter(champion = prime_hero_obj, ally_heroes = eval_hero_obj, item = item_obj, winner = True).count()
#             total = Player.objects.filter(champion = prime_hero_obj, ally_heroes = eval_hero_obj, item = item_obj).count()
#         elif created and not ally_bool:
#             wins = Player.objects.filter(champion = prime_hero_obj, enemy_heroes = eval_hero_obj, item = item_obj, winner = True).count()
#             total = Player.objects.filter(champion = prime_hero_obj, enemy_heroes = eval_hero_obj, item = item_obj).count()

#         if total != 0:
#             node.save()

#         return node

OUTPUT_SET_INT = 1

class MLPTrainerManager(NetworkTrainerManager):

    def __init__(self, player_object):

        if not isinstance(player_object, Player):
            raise ValueError('Object: ', player_object, ' is not a Player Object')

        super(MLPTrainerManager, self).__init__()            

        self.prime = player_object

        self.node_set_list = self.build_node_list()

        self.input_layer = LinearLayer(len(self.node_set_list), name = 'input_layer')
        self.hidden_layer = SigmoidLayer(len(self.node_set_list), name = 'hidden_layer')
        self.output_layer = SigmoidLayer(OUTPUT_SET_INT, name = 'win_layer')
        self.bias = BiasUnit()
        self.input_hidden_connection = FullConnection(self.input_layer, self.hidden_layer, name = 'input_hidden_connection')
        self.hidden_output_connection = FullConnection(self.hidden_layer, self.output_layer, name = 'hidden_output_connection')
        self.bias_hidden_connection = FullConnection(self.bias, self.hidden_layer, name = 'bias_connection')

        self.build_network()
        self.train_network()
        self.run_network()


    def build_network(self):
        self.network.addInputModule(self.input_layer)
        self.network.addModule(self.hidden_layer)    
        self.network.addOutputModule(self.output_layer)   
        self.network.addModule(self.bias)            
        self.network.addConnection(self.input_hidden_connection)
        self.network.addConnection(self.bias_hidden_connection)
        self.network.addConnection(self.hidden_output_connection)
        self.network.sortModules()
        print self.network

    def get_node(self, prime_hero_obj, eval_hero_obj, ally_bool, item_obj):

        if ally_bool:
            node, created = ItemAllyNode.objects.get_or_create(prime = prime_hero_obj, ally = eval_hero_obj, item = item_obj)
        else:
            node, created = ItemEnemyNode.objects.get_or_create(prime = prime_hero_obj, enemy = eval_hero_obj, item = item_obj)

        return node, created

    def build_node_list(self):

        ally_node_list = []
        enemy_node_list = []
        self.ally_validator_list = []
        self.enemy_validator_list = []

        print '------------ %s -------------' % self.prime
        
        for p_ally in self.prime.ally_players.all():
            champion = p_ally.champion
            self.ally_validator_list.append(champion)
            for i in self.prime.item.all():
                node, created = self.get_node(self.prime.champion, champion, True, i)
                
                current_total = Player.objects.filter(champion = node.prime, ally_heroes = champion, item = i).count()
                
                # if current_total < 10:
                #     continue

                if created:
                    ally_node_list.append(node)
                    node.wins = Player.objects.filter(champion = node.prime, ally_heroes = champion, item = i, winner = True).count()
                    node.total = current_total
                    node.save()
                else:
                    ally_node_list.append(node)
                    node.total = current_total
                    node.wins = Player.objects.filter(champion = node.prime, ally_heroes = champion, item = i, winner = True).count()
                    # node.weight = 0.5 #TEMP -  Set up right now to re-run all matches, so needs to start from scratch.  Need an weight update function.
                    node.save()

        for p_enemy in self.prime.enemy_players.all():
            champion = p_enemy.champion
            self.enemy_validator_list.append(champion)
            for i in p_enemy.item.all():
                node, created = self.get_node(self.prime.champion, champion, False, i)
                
                current_total = Player.objects.filter(champion = node.prime, enemy_heroes = champion, item = i).count()
                
                # if current_total < 10:
                #     continue

                if created:
                    enemy_node_list.append(node)
                    node.wins = Player.objects.filter(champion = node.prime, enemy_heroes = champion, item = i, winner = True).count()
                    node.total = current_total
                    node.save()
                else:
                    enemy_node_list.append(node)
                    node.total = current_total
                    node.wins = Player.objects.filter(champion = node.prime, enemy_heroes = champion, item = i, winner = True).count()
                    # node.weight = 0.5 #TEMP -  Set up right now to re-run all matches, so needs to start from scratch.  Need an weight update function.
                    node.save()


                
        return ally_node_list+enemy_node_list

    def train_network(self):

        node_average_num = 0.0
        node_average_denom = 0.0

        training_set = SupervisedDataSet(len(self.node_set_list), OUTPUT_SET_INT)

        for i in xrange(0, len(self.node_set_list)):
            node = self.node_set_list[i]
            input_set = [0]*len(self.node_set_list)
            input_set[i] = 1
            node_average_num += float(node.wins)
            node_average_denom += float(node.total)
            # try:
            #     node.ally
            #     print 'This is Ally Node: ', node.ally
            # except:
            #     print 'This is Enemy Node: ', node.enemy
            # try:
            #     average = float(node.wins)/float(node.total)
            #     print 'Node Average = %s / %s = ' %(node.wins, node.total), average
            # except:
            #     pass

            j = 1
            k = 1

            while j <= node.wins:
                training_set.addSample(input_set, [1])
                j+=1
            while k <= (node.total - node.wins):
                training_set.addSample(input_set, [0])
                k+=1
        print 'Length of Dataset = ', len(training_set)
        print 'TRAINING.......'
        print "PRIOR TO TRANING WEIGHTS.... ", self.network.params
        trainer = BackpropTrainer(self.network, training_set)
        trainer.trainEpochs(epochs = len(training_set))

        #trainer.trainUntilConvergence(verbose = True)
        print 'Number of Nodes = ', len(self.node_set_list)
        print "Pure Average = %s / %s = "%(node_average_num,node_average_denom), node_average_num/node_average_denom
        print '---------------------------------'

    def run_network(self):
        print 'AFTER TRAINING WEIGHTS..... ', self.network.params
        input_set = [1]*len(self.node_set_list)
        print self.network.activate(input_set)
        print 'Allies: ', self.prime.ally_heroes
        print 'Enemies: ', self.prime.enemy_heroes
        print "Winner? ", self.prime.winner
        champion = self.prime.champion
        a_h = self.prime.ally_heroes.all()
        e_h = self.prime.enemy_heroes.all()
        print champion
        print a_h
        print e_h
        matches = Player.objects.filter(champion = champion, ally_heroes = a_h , enemy_heroes = e_h).count()
        won_matches = Player.objects.filter(champion = champion, ally_heroes = a_h , enemy_heroes = e_h , winner = True).count()
        print '# Matches of Input: ',matches
        print '# of Wins: ', won_matches
        print 'Win % = %s %', float(won_matches)/float(matches)*100








class PrimeLinearTrainerManager(NetworkTrainerManager):

    def __init__(self, player_object):

        if not isinstance(player_object, Player):
            raise ValueError('Object: ', player_object, ' is not a Player Object')

        super(PrimeLinearTrainerManager, self).__init__()            

        self.prime = player_object 

        self.training_node_set_list = self.build_training_node_list() #Training Node List does not include any node that does not need additional training.       

        self.input_layer = LinearLayer(1, name = 'item_layer')
        self.input = [1]
        self.output_layer = LinearLayer(1, name = 'win_layer')
        self.linear_connection = FullConnection(self.input_layer, self.output_layer, name = 'c1')
        
        



    def train_linear_network(self):

        for node in self.training_node_set_list:

            # self.reset_weight_for_training(node)
            network = self.build_training_network(node)
            data_set = SupervisedDataSet(1, 1)

            if node.total < 1: #No Training for nodes with less then 1 datapoints
                continue
            
            print 'TOTAL = ', node.total
            print 'WINS = ', node.wins
            print 'LOSS = ', node.total - node.wins
            print 'NETWORK PARAMS BEFORE TRAINING = ', network.params
            target_set = [0]*(node.total-node.wins)+[1]*node.wins
            print target_set

            for i in target_set:
                data_set.appendLinked([1],i)

                
            self.train(network, data_set, node)
            print 'NETWORK PARAMS AFTER TRAINING = ', network.params



    def get_node(self, prime_hero_obj, eval_hero_obj, ally_bool, item_obj):

        if ally_bool:
            node, created = ItemAllyNode.objects.get_or_create(prime = prime_hero_obj, ally = eval_hero_obj, item = item_obj)
        else:
            node, created = ItemEnemyNode.objects.get_or_create(prime = prime_hero_obj, enemy = eval_hero_obj, item = item_obj)

        return node, created

    def build_training_network(self, node):

        network = FeedForwardNetwork()

        network.addInputModule(self.input_layer)    
        network.addOutputModule(self.output_layer)               
        network.addConnection(self.linear_connection)
        network.sortModules()

        network._setParameters([node.weight])

        return network




    def build_training_node_list(self):

        ally_node_list = []
        enemy_node_list = []

        for p_ally in self.prime.ally_players.all():
            champion = p_ally.champion
            for i in self.prime.item.all():
                node, created = self.get_node(self.prime.champion, champion, True, i)
                
                current_total = Player.objects.filter(champion = node.prime, ally_heroes = champion, item = i).count()
                if created:
                    ally_node_list.append(node)
                    node.wins = Player.objects.filter(champion = node.prime, ally_heroes = champion, item = i, winner = True).count()
                    node.total = current_total
                    node.save()
                elif node.total < current_total:
                    ally_node_list.append(node)
                    node.total = current_total
                    node.wins = Player.objects.filter(champion = node.prime, ally_heroes = champion, item = i, winner = True).count()
                    node.weight = 0.5 #TEMP -  Set up right now to re-run all matches, so needs to start from scratch.  Need an weight update function.
                    node.save()



        for p_enemy in self.prime.enemy_players.all():
            champion = p_enemy.champion
            for i in p_enemy.item.all():
                node, created = self.get_node(self.prime.champion, champion, False, i)
                
                current_total = Player.objects.filter(champion = node.prime, enemy_heroes = champion, item = i).count()
                if created:
                    enemy_node_list.append(node)
                    node.wins = Player.objects.filter(champion = node.prime, enemy_heroes = champion, item = i, winner = True).count()
                    node.total = current_total
                    node.save()
                elif node.total < current_total:
                    enemy_node_list.append(node)
                    node.total = current_total
                    node.wins = Player.objects.filter(champion = node.prime, enemy_heroes = champion, item = i, winner = True).count()
                    node.weight = 0.5 #TEMP -  Set up right now to re-run all matches, so needs to start from scratch.  Need an weight update function.
                    node.save()


                
        return ally_node_list+enemy_node_list                       












