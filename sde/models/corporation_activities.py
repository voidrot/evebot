from django.db import models


class CorporationActivity(models.Model):
    id = models.IntegerField(primary_key=True)
    name_id = models.JSONField()

    def __str__(self):
        return f"{self.name_id["en"]}"
