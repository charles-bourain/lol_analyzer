from django.db import models

class Mastery(models.Model):

    masteryId = models.IntegerField(blank = False, null = True)
    name = models.SlugField()
    description = models.CharField(max_length = 200)

    def __unicode__(self):
        return unicode(self.name)


class PlayerMastery(models.Model):
    mastery = models.ForeignKey(Mastery)
    rank = models.IntegerField()
