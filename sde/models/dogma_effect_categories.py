from django.db import models


class DogmaEffectCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()

    def __str__(self):
        return f"{self.name}"
