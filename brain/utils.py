from .models import AllyNode, EnemyNode
from matches.models import Player, Match
from pybrain.structure import FeedForwardNetwork, FullConnection



def build_network(match_obj):

    player_list = Player.objects.filter(match = match_obj)

    node_obj_list = []

    for player in player_list:
        for p_ally in player.ally_players.all():
            champion = p_ally.champion
            for i in player.item.all():
                node_obj_list.append(get_node(player.champion, champion, True, i))

        for p_enemy in player.enemy_players.all():
            champion = p_enemy.champion
            for i in p_enemy.item.all():
                node_obj_list.append(get_node(player.champion, champion, False, i))

    #defining neural network
    network = FeedForwardNetwork()
    input_layer = LinearLayer(len(node_obj_list))
    output_layer = LinearLayer(1)
    input_output_connection = FullConnection(input_layer, output_layer)

    network.addInputModule(input_layer)
    network.addOutputModule(output_layer)
    network.addConnection(input_output_connection)
    network.sortModules()

    input_list = []
    weight_list = []
    for node in node_obj_list:
        input_list.append(node.win_rate)
        weight_list.append(node.weight)

    input_output_connection.params = weight_list
    print network.active(input_list)









#Getting strange false items in this function.  item_obj is appear, but when Player.objects.filter is called, total = 0 in some cases.  Possible sold item?
def get_node(prime_hero_obj, eval_hero_obj, ally_bool, item_obj):

    if ally_bool:
        node, created = AllyNode.objects.get_or_create(prime = prime_hero_obj, ally = eval_hero_obj, item = item_obj)
    else:
        node, created = EnemyNode.objects.get_or_create(prime = prime_hero_obj, enemy = eval_hero_obj, item = item_obj)
    
    if created and ally_bool:
        wins = Player.objects.filter(champion = prime_hero_obj, ally_heroes = eval_hero_obj, item = item_obj, winner = True).count()
        total = Player.objects.filter(champion = prime_hero_obj, ally_heroes = eval_hero_obj, item = item_obj).count()
    elif created and not ally_bool:
        wins = Player.objects.filter(champion = prime_hero_obj, enemy_heroes = eval_hero_obj, item = item_obj, winner = True).count()
        total = Player.objects.filter(champion = prime_hero_obj, enemy_heroes = eval_hero_obj, item = item_obj).count()

    if total != 0:
        node.win_rate = float(wins)/float(total)
        node.save()

    return node


def test_build_network():
    AllyNode.objects.all().delete()
    EnemyNode.objects.all().delete()
    build_network(Match.objects.get(id = 5000))




