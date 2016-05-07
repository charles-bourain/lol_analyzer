from .models import *
from matches.models import Player, Match
from pybrain.structure import FeedForwardNetwork, FullConnection, LinearLayer, SigmoidLayer, RecurrentNetwork
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




class PrimeTrainingNetworkManager(NetworkTrainerManager):

    def __init__(self, player_object):

        if not isinstance(player_object, Player):
            raise ValueError('Object: ', player_object, ' is not a Player Object')

        super(PrimeTrainingNetworkManager, self).__init__()            

        self.prime = player_object

        ally_node_list = []
        enemy_node_list = []

        for p_ally in self.prime.ally_players.all():
            champion = p_ally.champion
            for i in self.prime.item.all():
                node = self.get_node(self.prime.champion, champion, True, i)
                ally_node_list.append(node)

        for p_enemy in self.prime.enemy_players.all():
            champion = p_enemy.champion
            for i in p_enemy.item.all():
                node = self.get_node(self.prime.champion, champion, False, i)
                enemy_node_list.append(node)        

        self.input_layer = LinearLayer(len(ally_node_list+enemy_node_list), name = 'item_layer')
        self.input = [1]*len(ally_node_list+enemy_node_list)
        self.output_layer = LinearLayer(1, name = 'win_layer')
        self.linear_connection = FullConnection(self.input_layer, self.output_layer, name = 'c1')

        if self.prime.winner:
            self.target = [1]
        else:
            self.target = [0]
        
        self.node_set_list = ally_node_list+enemy_node_list

        self.build_network()


    def get_node(self, prime_hero_obj, eval_hero_obj, ally_bool, item_obj):

        if ally_bool:
            node, created = ItemAllyNode.objects.get_or_create(prime = prime_hero_obj, ally = eval_hero_obj, item = item_obj)
        else:
            node, created = ItemEnemyNode.objects.get_or_create(prime = prime_hero_obj, enemy = eval_hero_obj, item = item_obj)

        total = 0
        
        if created and ally_bool:
            wins = Player.objects.filter(champion = prime_hero_obj, ally_heroes = eval_hero_obj, item = item_obj, winner = True).count()
            total = Player.objects.filter(champion = prime_hero_obj, ally_heroes = eval_hero_obj, item = item_obj).count()
        elif created and not ally_bool:
            wins = Player.objects.filter(champion = prime_hero_obj, enemy_heroes = eval_hero_obj, item = item_obj, winner = True).count()
            total = Player.objects.filter(champion = prime_hero_obj, enemy_heroes = eval_hero_obj, item = item_obj).count()

        if total != 0:
            node.save()

        return node


class PrimeLinearTrainerManager(NetworkTrainerManager):

    def __init__(self, player_object):

        if not isinstance(player_object, Player):
            raise ValueError('Object: ', player_object, ' is not a Player Object')

        super(PrimeLinearTrainerManager, self).__init__()            

        self.prime = player_object

        ally_node_list = []
        enemy_node_list = []

        for p_ally in self.prime.ally_players.all():
            champion = p_ally.champion
            for i in self.prime.item.all():
                node = self.get_node(self.prime.champion, champion, True, i)
                ally_node_list.append(node)

        for p_enemy in self.prime.enemy_players.all():
            champion = p_enemy.champion
            for i in p_enemy.item.all():
                node = self.get_node(self.prime.champion, champion, False, i)
                enemy_node_list.append(node)        

        self.input_layer = LinearLayer(1, name = 'item_layer')
        self.input = [1]
        self.output_layer = LinearLayer(1, name = 'win_layer')
        self.linear_connection = FullConnection(self.input_layer, self.output_layer, name = 'c1')
        
        self.node_set_list = ally_node_list+enemy_node_list



    def train_linear_network(self):

        for node in self.node_set_list:

            self.reset_weight_for_training(node)
            network = self.build_training_network(node)
            data_set = SupervisedDataSet(1, 1)
            

            try:

                ally = node.ally
                loss = Player.objects.filter(champion = node.prime, ally_heroes = ally, item = node.item, winner = False).count()
                wins = Player.objects.filter(champion = node.prime, ally_heroes = ally, item = node.item, winner = True).count()

            except:
                enemy = node.enemy
                loss = Player.objects.filter(champion = node.prime, ally_heroes = ally, item = node.item, winner = False).count()
                wins = Player.objects.filter(champion = node.prime, ally_heroes = ally, item = node.item, winner = True).count()

            if loss+wins == 0:
                continue
                print 'PASSING..'


            print 'WINS = ', wins
            print 'LOSS = ', loss
            print 'NETWORK PARAMS BEFORE TRAINING = ', network.params
            target_set = [0]*loss+[1]*wins
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

        return node

    def build_training_network(self, node):

        network = FeedForwardNetwork()

        network.addInputModule(self.input_layer)    
        network.addOutputModule(self.output_layer)               
        network.addConnection(self.linear_connection)
        network.sortModules()

        network._setParameters([node.weight])

        return network

    def reset_weight_for_training(self,node):
        node.weight = 0.5
        node.save()








