from django.db import models


class Ancestry(models.Model):
    id = models.IntegerField(primary_key=True)
    bloodline_id = models.IntegerField()
    description = models.TextField()
    icon_id = models.IntegerField()
    name = models.TextField()
    short_description = models.TextField()
    charisma = models.IntegerField()
    intelligence = models.IntegerField()
    memory = models.IntegerField()
    perception = models.IntegerField()
    willpower = models.IntegerField()
