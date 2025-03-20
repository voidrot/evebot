from django.db import models


class Agent(models.Model):
    id = models.IntegerField(primary_key=True)
    agent_type_id = models.IntegerField()
    corporation_id = models.IntegerField()
    division_id = models.IntegerField()
    is_locator = models.BooleanField()
    level = models.IntegerField()
    location_id = models.IntegerField()

    def __str__(self):
        return f"{self.id}"
