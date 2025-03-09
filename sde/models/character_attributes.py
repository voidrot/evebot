from django.db import models


class CharacterAttribute(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.TextField()
    icon_id = models.IntegerField()
    name_id = models.JSONField()
    notes = models.TextField()
    short_description = models.TextField()

    def __str__(self):
        return f"{self.name_id["en"]}"
