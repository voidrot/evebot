from django.db import models


class Debuff(models.Model):
    id = models.IntegerField(primary_key=True)
    name_id = models.IntegerField(null=True, default=None)
    location_group_modifiers = models.JSONField(default=list)
    description = models.TextField()
    operation_name = models.TextField()
    location_modifiers = models.JSONField(default=list)
    location_required_skill_modifiers = models.JSONField(default=list)
    item_modifiers = models.JSONField(default=list)
    aggregate_mode = models.TextField()
    show_output_value_in_ui = models.TextField()

    def __str__(self):
        return f"{self.name_id}"
