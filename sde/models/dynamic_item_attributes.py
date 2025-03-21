from django.db import models


class DynamicItemAttribute(models.Model):
    id = models.IntegerField(primary_key=True)
    input_output_mapping = models.JSONField(default=list)
    attribute_ids = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.id}"
