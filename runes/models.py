from django.db import models

class Rune(models.Model):

    runeId = models.IntegerField(blank = False, null = True)
    description = models.CharField(max_length = 2000)
    name = models.SlugField(max_length = 200)

    def __unicode__(self):
        return unicode(self.name)


class PlayerRune(models.Model):

    rune = models.ForeignKey(Rune)
    rank = models.IntegerField()
