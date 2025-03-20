from django.db import models


class Landmark(models.Model):
    id = models.IntegerField(primary_key=True)
    description_id = models.IntegerField()
    landmark_name_id = models.IntegerField()
    position = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.landmark_name_id}"
