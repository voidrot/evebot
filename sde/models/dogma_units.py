from django.db import models

class DogmaUnit(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    description = models.TextField(null=True, default=None)
    display_name = models.TextField(null=True, default=None)

    def __str__(self):
        return f"{self.name}"
