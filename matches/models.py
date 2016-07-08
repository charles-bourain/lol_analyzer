from django.db import models
from heroes.models import Hero
from runes.models import Rune
from masteries.models import Mastery
from items.models import Item


# To Gather Initial Data:
#   A) Riot.API.get a list of players in MASTERS league (1 request)
#   B) Create database of player IDs from A) (0 requests)
#   C) For each summoner gathered in B), perform API request to get a list of matches(Requests = # player ids)
#   D) Gather match IDs for each list from C) (0 Requests)
#   E) Riot.API.get match details (Requests = # of match played by each player) (Repeats are ignored)






class Match(models.Model):
    match_id = models.SlugField()
    blue_champion_1 = models.ForeignKey(Hero, related_name = 'blue_champion_1', null = True, blank = True)
    blue_items_1 = models.ManyToManyField(Item, related_name = 'blue_items_1', blank = True)
    blue_champion_2 = models.ForeignKey(Hero, related_name = 'blue_champion_2', null = True, blank = True)
    blue_items_2 = models.ManyToManyField(Item, related_name = 'blue_items_2', blank = True)
    blue_champion_3 = models.ForeignKey(Hero, related_name = 'blue_champion_3', null = True, blank = True)
    blue_items_3 = models.ManyToManyField(Item, related_name = 'blue_items_3', blank = True)
    blue_champion_4 = models.ForeignKey(Hero, related_name = 'blue_champion_4', null = True, blank = True)
    blue_items_4 = models.ManyToManyField(Item, related_name = 'blue_items_4', blank = True)
    blue_champion_5 = models.ForeignKey(Hero, related_name = 'blue_champion_5', null = True, blank = True)
    blue_items_5 = models.ManyToManyField(Item, related_name = 'blue_items_5', blank = True)
    red_champion_1 = models.ForeignKey(Hero, related_name = 'red_champion_1', null = True, blank = True)
    red_items_1 = models.ManyToManyField(Item, related_name = 'red_items_1', blank = True)
    red_champion_2 = models.ForeignKey(Hero, related_name = 'red_champion_2', null = True, blank = True)
    red_items_2 = models.ManyToManyField(Item, related_name = 'red_items_2', blank = True)
    red_champion_3 = models.ForeignKey(Hero, related_name = 'red_champion_3', null = True, blank = True)
    red_items_3 = models.ManyToManyField(Item, related_name = 'red_items_3', blank = True) 
    red_champion_4 = models.ForeignKey(Hero, related_name = 'red_champion_4', null = True, blank = True)
    red_items_4 = models.ManyToManyField(Item, related_name = 'red_items_4', blank = True)
    red_champion_5 = models.ForeignKey(Hero, related_name = 'red_champion_5', null = True, blank = True)
    red_items_5 = models.ManyToManyField(Item, related_name = 'red_items_5', blank = True)

    winning_team = models.IntegerField(null = True) # 100 is Blue Team Winner



    def __unicode__(self):
            return "Match ID: "+unicode(self.match_id)

# class Player(models.Model):  

#     match = models.ForeignKey(Match)
#     champion = models.ForeignKey(Hero)
#     runes = models.ManyToManyField(Rune)
#     rune_rank = models.CharField(max_length = 1000)
#     masteries = models.ManyToManyField(Mastery)
#     mastery_rank = models.CharField(max_length = 1000)
#     item = models.ManyToManyField(Item)
#     winner = models.BooleanField(default = False)
#     json_response = models.CharField(max_length = 10000)
#     spell1 = models.IntegerField(default = 666)
#     spell2 = models.IntegerField(default = 666)
#     team = models.IntegerField()
#     ally_heroes = models.ManyToManyField(Hero, related_name = 'allies')
#     enemy_heroes = models.ManyToManyField(Hero, related_name = 'enemies')
#     ally_players = models.ManyToManyField('self')
#     enemy_players = models.ManyToManyField('self')

#     totalDamageTaken = models.IntegerField(default = 0)
#     physicalDamageTaken = models.IntegerField(default = 0)
#     magicDamageTaken = models.IntegerField(default = 0)

#     sightWardsBoughtInGame = models.IntegerField(default = 0)
#     visionWardsBoughtInGame = models.IntegerField(default = 0)
#     wardsKilled = models.IntegerField(default = 0)
#     wardsPlaced = models.IntegerField(default = 0)
    
#     deaths = models.IntegerField(default = 0)
#     assists = models.IntegerField(default = 0)
#     kills = models.IntegerField(default = 0)
    
#     firstBloodAssist = models.BooleanField(default = False)
    
#     magicDamageDealtToChampions =  models.IntegerField(default = 0)
#     physicalDamageDealtToChampions = models.IntegerField(default = 0)
#     totalDamageDealtToChampions = models.IntegerField(default = 0)
#     totalTimeCrowdControlDealt = models.IntegerField(default = 0)

#     minionsKilled = models.IntegerField(default = 0)
#     goldEarned = models.IntegerField(default = 0)

#     totalHeal = models.IntegerField(default = 0)
 
#     def __unicode__(self):
#         return unicode(self.match.id) +" "+ unicode(self.champion)


