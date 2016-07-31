from django.db import models

# Create your models here.

class Hero(models.Model):
    name = models.CharField(max_length = 20)
    riot_id = models.IntegerField(default = 1)
    image_name = models.CharField(null = True, blank = True, max_length = 20)
    # tag = models.CharField(max_length = 20)
    attackrange = models.FloatField(default = 1)
    mpperlevel = models.FloatField(default = 1)
    mp = models.FloatField(default = 1)
    attackdamage = models.FloatField(default = 1)
    hp = models.FloatField(default = 1)
    hpperlevel = models.FloatField(default = 1)
    attackdamageperlevel = models.FloatField(default = 1)
    armor = models.FloatField(default = 1)
    mpregenperlevel = models.FloatField(default = 1)
    hpregen = models.FloatField(default = 1)
    critperlevel = models.FloatField(default = 1)
    spellblockperlevel = models.FloatField(default = 1)
    mpregen = models.FloatField(default = 1)
    attackspeedperlevel = models.FloatField(default = 1)
    spellblock = models.FloatField(default = 1)
    movespeed = models.FloatField(default = 1)
    attackspeedoffset = models.FloatField(default = 1)
    crit = models.FloatField(default = 1)
    hpregenperlevel = models.FloatField(default = 1)
    armorperlevel = models.FloatField(default = 1)
      
    def __unicode__(self):
        return unicode(self.name)