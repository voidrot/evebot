from django.db import models

class IndustryTargetFilter(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    category_ids = models.JSONField(default=list)
    group_ids = models.JSONField(default=list)

    def __str__(self):
        return f"{self.name}"
