from django.db import models


class AgentsInSpace(models.Model):
    id = models.IntegerField(primary_key=True)
    dungeon_id = models.IntegerField()
    solar_system_id = models.IntegerField()
    spawn_point_id = models.IntegerField()
    type_id = models.IntegerField()

    def __str__(self):
        return f"{self.id}"
