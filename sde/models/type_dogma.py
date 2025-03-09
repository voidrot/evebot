from django.db import models


class TypeDogma(models.Model):
    id = models.IntegerField(primary_key=True)
    dogma_attributes = models.JSONField()
    dogma_effects = models.JSONField()

    def __str__(self):
        return f"{self.id}"
