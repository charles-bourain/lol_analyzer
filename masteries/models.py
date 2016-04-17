from django.db import models

class Mastery(models.Model):

    masteryId = models.IntegerField(blank = False, null = True)
    description = models.CharField(max_length = 10000)
    name = models.SlugField(max_length = 1000)

    def __unicode__(self):
        return unicode(self.name)


class PlayerMastery(models.Model):
    mastery = models.ForeignKey(Mastery)
    rank = models.IntegerField()
