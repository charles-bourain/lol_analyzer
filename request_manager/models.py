from django.db import models

class Request(models.Model):

    request_time = models.DateTimeField(auto_now = True)
    
    def __unicode__(self):
            return unicode(self.request_time)    