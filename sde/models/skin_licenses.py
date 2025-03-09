from django.db import models


class SkinLicense(models.Model):
    id = models.IntegerField(primary_key=True)
    duration = models.IntegerField()
    license_type_id = models.IntegerField()
    skin_id = models.IntegerField()
    is_single_use = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.id}"
