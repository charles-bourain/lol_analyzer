from django.db import models

class Rune(models.Model):

    runeId = models.IntegerField(blank = False, null = True)
    description = models.CharField(max_length = 10000)
    name = models.SlugField(max_length = 1000)

    def __unicode__(self):
        return unicode(self.name)
