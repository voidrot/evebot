from django.db import models


class Ancestry(models.Model):
    id = models.IntegerField(primary_key=True)
    bloodline_id = models.IntegerField()
    charisma = models.IntegerField()
    description_id = models.JSONField()
    icon_id = models.IntegerField(default=None, null=True, blank=True)
    intelligence = models.IntegerField()
    memory = models.IntegerField()
    name_id = models.JSONField()
    perception = models.IntegerField()
    short_description = models.TextField(null=True, default=None)
    willpower = models.IntegerField()

    def __str__(self):
        return f"{self.name_id['en']}"
