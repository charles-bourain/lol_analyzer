from django.db import models
from heroes.models import Hero

# Create your models here.
class Item(models.Model):
	name = models.CharField(max_length = 50)
	riot_id = models.IntegerField()
	tag = models.CharField(max_length = 100)
	counter_hero = models.ForeignKey(Hero, related_name = 'counter', blank = True, null = True)
	for_hero = models.ForeignKey(Hero, blank = True, null = True)

class ItemTag(models.Model):
	item = models.ForeignKey(Item)
	tag = models.CharField(max_length = 20)
