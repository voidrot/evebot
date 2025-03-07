from django.db import models


class Bloodline(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    description = models.TextField()
    corporation_id = models.IntegerField()
    icon_id = models.IntegerField()
    race_id = models.IntegerField()
    charisma = models.IntegerField()
    intelligence = models.IntegerField()
    memory = models.IntegerField()
    perception = models.IntegerField()
    willpower = models.IntegerField()
