from django.db import models


class Bloodline(models.Model):
    id = models.IntegerField(primary_key=True)
    charisma = models.IntegerField()
    corporation_id = models.IntegerField()
    description_id = models.JSONField()
    icon_id = models.IntegerField(default=None, null=True, blank=True)
    intelligence = models.IntegerField()
    memory = models.IntegerField()
    name_id = models.JSONField()
    perception = models.IntegerField()
    race_id = models.IntegerField()
    willpower = models.IntegerField()

    def __str__(self):
        return f"{self.name_id['en']}"
