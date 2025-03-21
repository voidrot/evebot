from django.db import models


class IndustryActivity(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"
