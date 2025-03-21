from django.db import models


class CloneState(models.Model):
    id = models.IntegerField(primary_key=True)
    skills = models.JSONField(default=dict)
    name = models.TextField()

    def __str__(self):
        return f"{self.name}"
