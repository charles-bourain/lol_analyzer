from django.db import models
from heroes.models import Hero
from items.models import Item
from masteries.models import Mastery
from picklefield.fields import PickledObjectField

# Create your models here.

class DataPickler(models.Model):
    data = PickledObjectField(editable = True)
