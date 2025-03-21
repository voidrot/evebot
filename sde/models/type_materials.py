from django.db import models


class TypeMaterial(models.Model):
    id = models.IntegerField(primary_key=True)
    materials = models.JSONField(default=list)

    def __str__(self):
        return f"{self.id}"
