from django.db import models


class School(models.Model):
    id = models.IntegerField(primary_key=True)
    corporation_id = models.IntegerField()
    career_id = models.IntegerField()
    race_id = models.IntegerField()
    icon_id = models.IntegerField(null=True, default=None)
    name = models.TextField(null=True, default=None)  # noqa: DJ001
    internal_name = models.TextField(null=True, default=None)  # noqa: DJ001
    description = models.TextField()
    starting_stations = models.JSONField(default=list, null=True)

    def __str__(self):
        return f"{self.name}"
