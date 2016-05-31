from .models import *
from matches.models import Player, Match
from pybrain.structure import FeedForwardNetwork, FullConnection, LinearLayer, SigmoidLayer, RecurrentNetwork, BiasUnit, TanhLayer
from pybrain.supervised.trainers import BackpropTrainer, RPropMinusTrainer # trainer = BackpropTrainer(network, dataset)
from pybrain.datasets.supervised import SupervisedDataSet
from pybrain.tools.neuralnets import NNregression


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


#This Manager is currently building node-sets ignoring items - datasets are not robust enough
class MLPTrainerManager(NetworkTrainerManager):

    def __init__(self, player_object):

        if not isinstance(player_object, Player):
            raise ValueError('Object: ', player_object, ' is not a Player Object')

        super(MLPTrainerManager, self).__init__()            

        self.prime = player_object

        self.node_set_list = self.build_node_list()

        self.input_layer = LinearLayer(len(self.node_set_list), name = 'input_layer')
        self.hidden_layer1 = TanhLayer(len(self.node_set_list), name = 'hidden1_layer')
        self.hidden_layer2 = TanhLayer(len(self.node_set_list), name = 'hidden2_layer')
        self.output_layer = SigmoidLayer(1, name = 'win_layer')
        self.bias_hidden1 = BiasUnit()
        self.bias_hidden2 = BiasUnit()
        self.bias_output = BiasUnit()
        self.input_hidden1_connection = FullConnection(self.input_layer, self.hidden_layer1, name = 'input_hidden1_connection')
        # self.hidden1_output_connection = FullConnection(self.hidden_layer1, self.output_layer, name = 'hidden1_output_connection')
        self.hidden1_hidden2_connection = FullConnection(self.hidden_layer1, self.hidden_layer2, name = 'hidden1_hidden2_connection')
        self.hidden2_output_connection = FullConnection(self.hidden_layer2, self.output_layer, name = 'hidden2_output_connection')
        self.bias_hidden1_connection = FullConnection(self.bias_hidden1, self.hidden_layer1, name = 'bias_hidden1_connection')
        self.bias_hidden2_connection = FullConnection(self.bias_hidden2, self.hidden_layer2, name = 'bias_hidden2_connection')
        self.bias_output_connection = FullConnection(self.bias_output, self.output_layer, name = 'bias_hidden2_connection')

        self.build_network()
        self.train_network()


    def build_network(self):
        self.network.addInputModule(self.input_layer)
        self.network.addModule(self.hidden_layer1)
        self.network.addModule(self.hidden_layer2)      
        self.network.addOutputModule(self.output_layer)   
        self.network.addModule(self.bias_hidden1) 
        self.network.addModule(self.bias_hidden2)
        self.network.addModule(self.bias_output)            
        self.network.addConnection(self.input_hidden1_connection)
        self.network.addConnection(self.hidden1_hidden2_connection)
        self.network.addConnection(self.hidden2_output_connection)
        # self.network.addConnection(self.hidden1_output_connection)        
        self.network.addConnection(self.bias_hidden1_connection)
        self.network.addConnection(self.bias_hidden2_connection)
        self.network.addConnection(self.bias_output_connection)

        self.network.sortModules()

    def get_node(self, prime_hero_obj, eval_hero_obj, ally_bool, item_obj):

        if ally_bool:
            node, created = ItemAllyNode.objects.get_or_create(prime = prime_hero_obj, ally = eval_hero_obj, item = item_obj)
        else:
            node, created = ItemEnemyNode.objects.get_or_create(prime = prime_hero_obj, enemy = eval_hero_obj, item = item_obj)

        return node, created
                
        return ally_node_list+enemy_node_list

#THIS FUNCTION HOLDS THE ITEM VERSION OF BUILD NODE LIST
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
                
                #If not created, then updated with queryset of node.wins
                if created:
                    ally_node_list.append(node)
                    node.wins = Player.objects.filter(champion = node.prime, ally_heroes = champion, winner = True, item = i).count()
                    node.total = current_total
                    node.save()
                else:
                    ally_node_list.append(node)
                    node.total = current_total
                    node.wins = Player.objects.filter(champion = node.prime, ally_heroes = champion, winner = True, item = i).count()
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

        lost_matches = Player.objects.filter(champion = self.prime.champion, ally_heroes = self.prime.ally_heroes.all() , enemy_heroes = self.prime.enemy_heroes.all(), winner = False)
        won_matches = Player.objects.filter(champion = self.prime.champion, ally_heroes = self.prime.ally_heroes.all() , enemy_heroes = self.prime.enemy_heroes.all() , winner = True)
        print self.prime.ally_heroes.all()
        print lost_matches[1].ally_heroes

        for item in self.prime.item.all():
            lost_matches = lost_matches.filter(item = item)
            won_matches = won_matches.filter(item = item)


        node_average_num = 0.0
        node_average_denom = 0.0

        training_set = SupervisedDataSet(len(self.node_set_list), 1)
        validation_set = SupervisedDataSet(len(self.node_set_list), 1)

        for i in xrange(0, len(self.node_set_list)):
            node = self.node_set_list[i]
            input_set = [0]*len(self.node_set_list)
            input_set[i] = 1
            node_average_num += float(node.wins)
            node_average_denom += float(node.total)

            j = 1
            k = 1

            while j <= node.wins:
                training_set.addSample(input_set, [1])
                j+=1
            while k <= (node.total - node.wins):
                training_set.addSample(input_set, [0])
                k+=1
        for i in won_matches:
            validation_set.addSample([1]*len(input_set), [1])
        for i in lost_matches:
            validation_set.addSample([1]*len(input_set), [0])
        print 'Length of Dataset = ', len(training_set)
        print 'length of valid set = ', len(validation_set)
        trainer = BackpropTrainer(self.network, learningrate = 0.5)

        trainer.trainUntilConvergence(validationData = validation_set, trainingData = training_set, continueEpochs = 10, maxEpochs = 100, convergence_threshold = 1)

    def run_network(self):

        for i in self.prime.item.all():
            won_matches = Player.objects.filter(champion = self.prime.champion, ally_heroes = self.prime.ally_heroes.all() , enemy_heroes = self.prime.enemy_heroes.all(), winner = True, item = i).count()
            matches = Player.objects.filter(champion = self.prime.champion, ally_heroes = self.prime.ally_heroes.all() , enemy_heroes = self.prime.enemy_heroes.all() , item = i).count()

        input_set = [1]*len(self.node_set_list)
        return self.network.activate(input_set)[0], str(float(won_matches)/float(matches))








class ChampionMLPTrainerManager(MLPTrainerManager):
    
    def build_node_list(self):

        ally_node_list = []
        enemy_node_list = []
        self.ally_validator_list = []
        self.enemy_validator_list = []

        print '------------ %s -------------' % self.prime
        
        TEMP_ITEM = Item.objects.get(id = 1)

        for p_ally in self.prime.ally_players.all():
            champion = p_ally.champion
            self.ally_validator_list.append(champion)
            node, created = self.get_node(self.prime.champion, champion, True, TEMP_ITEM)
            
            current_total = Player.objects.filter(champion = node.prime, ally_heroes = champion).count()
            
            #If not created, then updated with queryset of node.wins
            if created:
                ally_node_list.append(node)
                node.wins = Player.objects.filter(champion = node.prime, ally_heroes = champion, winner = True).count()
                node.total = current_total
                node.save()
            else:
                ally_node_list.append(node)
                node.total = current_total
                node.wins = Player.objects.filter(champion = node.prime, ally_heroes = champion, winner = True).count()
                # node.weight = 0.5 #TEMP -  Set up right now to re-run all matches, so needs to start from scratch.  Need an weight update function.
                node.save()

        for p_enemy in self.prime.enemy_players.all():
            champion = p_enemy.champion
            self.enemy_validator_list.append(champion)
            node, created = self.get_node(self.prime.champion, champion, False, TEMP_ITEM)
            
            current_total = Player.objects.filter(champion = node.prime, enemy_heroes = champion).count()
            
            # if current_total < 10:
            #     continue

            if created:
                enemy_node_list.append(node)
                node.wins = Player.objects.filter(champion = node.prime, enemy_heroes = champion, winner = True).count()
                node.total = current_total
                node.save()
            else:
                enemy_node_list.append(node)
                node.total = current_total
                node.wins = Player.objects.filter(champion = node.prime, enemy_heroes = champion, winner = True).count()
                # node.weight = 0.5 #TEMP -  Set up right now to re-run all matches, so needs to start from scratch.  Need an weight update function.
                node.save()


        
















