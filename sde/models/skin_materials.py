from django.db import models


class SkinMaterial(models.Model):
    id = models.IntegerField(primary_key=True)
    display_name_id = models.IntegerField()
    material_set_id = models.IntegerField()
    skin_material_id = models.IntegerField()

    def __str__(self):
        return f"{self.id}"
