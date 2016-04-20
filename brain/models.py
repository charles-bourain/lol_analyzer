from django.db import models
from heroes.models import Hero
from items.models import Item

# Create your models here.

class NeuralNode(models.Model):
    prime = models.ForeignKey(Hero)
    item = models.ForeignKey(Item)
    win_rate = models.FloatField(default = 0.50)
    weight = models.FloatField(default = 0.50)

#Win Neural Node to store PyBrain inputs.  Win% is Win rate of prime hero with ally on team
class AllyNode(NeuralNode):
    ally = models.ForeignKey(Hero)

    def __unicode__(self):
        return unicode(self.prime.name +' : '+ self.ally.name +' : '+ self.item.name)

#Win Neural Node to store PyBrain inputs.  Win% is Win rate of prime hero against enemy hero
class EnemyNode(NeuralNode):
    enemy = models.ForeignKey(Hero)

    def __unicode__(self):
        return unicode(self.prime.name +' : '+ self.enemy.name +' : '+ self.item.name)    