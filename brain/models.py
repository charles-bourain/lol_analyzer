from django.db import models
from heroes.models import Hero
from items.models import Item
from masteries.models import Mastery

# Create your models here.

class NeuralNode(models.Model):
    prime = models.ForeignKey(Hero)
    weight = models.FloatField(default = 0.5)



#------- Item Nodes --------
class ItemNode(NeuralNode):
    item = models.ForeignKey(Item)
    total = models.IntegerField(default = 0)
    wins = models.IntegerField(default = 0)


#Win Neural Node to store PyBrain inputs.  Win% is Win rate of prime hero with ally on team
class ItemAllyNode(ItemNode):
    ally = models.ForeignKey(Hero)

    def __unicode__(self):
        return unicode(self.prime.name +' : '+ self.ally.name +' : '+ self.item.name)

#Win Neural Node to store PyBrain inputs.  Win% is Win rate of prime hero against enemy hero
class ItemEnemyNode(ItemNode):
    enemy = models.ForeignKey(Hero)

    def __unicode__(self):
        return unicode(self.prime.name +' : '+ self.enemy.name +' : '+ self.item.name)        

#------- END Item Nodes --------


#------- Mastery Nodes --------
class MasteryNode(NeuralNode):
    mastery = models.ForeignKey(Mastery)

class MasteryAllyNode(MasteryNode):
    ally = models.ForeignKey(Hero)

    def __unicode__(self):
        return unicode(self.prime.name +' : '+ self.ally.name +' : '+ self.mastery.name)

#Win Neural Node to store PyBrain inputs.  Win% is Win rate of prime hero against enemy hero
class MasteryEnemyNode(MasteryNode):
    enemy = models.ForeignKey(Hero)

    def __unicode__(self):
        return unicode(self.prime.name +' : '+ self.enemy.name +' : '+ self.mastery.name) 
#------- END Mastery Nodes --------
