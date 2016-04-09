from django.db import models


# To Gather Initial Data:
#   A) Riot.API.get a list of players in MASTERS league (1 request)
#   B) Create database of player IDs from A) (0 requests)
#   C) For each summoner gathered in B), perform API request to get a list of matches(Requests = # player ids)
#   D) Gather match IDs for each list from C) (0 Requests)
#   E) Riot.API.get match details (Requests = # of match played by each player) (Repeats are ignored)


class Match(models.Model):
    match_id = models.PositiveIntegerField()

    def __unicode__(self):
            return "Match ID: "+unicode(self.match_id)