from django.db import models


class Certificate(models.Model):
    id = models.IntegerField(primary_key=True)
    group_id = models.IntegerField()
    name = models.TextField()
    recommended_for = models.JSONField(default=list, null=True, blank=True)
    skill_types = models.JSONField()
    description = models.TextField()

    def __str__(self):
        return f"{self.id}"
