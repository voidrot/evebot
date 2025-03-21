from django.db import models


class Bloodline(models.Model):
    id = models.IntegerField(primary_key=True)
    charisma = models.IntegerField()
    corporation_id = models.IntegerField()
    icon_id = models.IntegerField(default=None, null=True, blank=True)
    intelligence = models.IntegerField()
    memory = models.IntegerField()
    perception = models.IntegerField()
    race_id = models.IntegerField()
    willpower = models.IntegerField()
    description_id = models.JSONField()
    name_id = models.JSONField()

    def __str__(self):
        return f"{self.name_id['en']}"
