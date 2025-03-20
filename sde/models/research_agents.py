from django.db import models


class ResearchAgent(models.Model):
    id = models.IntegerField(primary_key=True)
    skills = models.JSONField()

    def __str__(self):
        return f"{self.id}"
