from django.db import models


class DogmaAttributeCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.TextField(default=None)
    name = models.TextField()

    def __str__(self):
        return f"{self.id}"
