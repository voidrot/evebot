from django.db import models


class Ancestry(models.Model):
    id = models.IntegerField(primary_key=True)
    bloodline_id = models.IntegerField()
    charisma = models.IntegerField()
    icon_id = models.IntegerField(default=None, null=True, blank=True)
    intelligence = models.IntegerField()
    memory = models.IntegerField()
    perception = models.IntegerField()
    willpower = models.IntegerField()
    description_id = models.JSONField()
    name_id = models.JSONField()
    short_description = models.TextField(null=True, default=None)  # noqa: DJ001

    def __str__(self):
        return f"{self.name_id['en']}"
