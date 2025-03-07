from django.db import models


class Blueprint(models.Model):
    id = models.IntegerField(primary_key=True)
    blueprint_type_id = models.IntegerField()
    max_production_limit = models.IntegerField()
    manufacturing_time = models.IntegerField()
    manufacturing_materials = models.JSONField(null=True, blank=True, default=list)
    manufacturing_products = models.JSONField(null=True, blank=True, default=list)
    manufacturing_skills = models.JSONField(null=True, blank=True, default=list)
    research_material_time = models.IntegerField()
    research_time = models.IntegerField()
    copying_time = models.IntegerField()
    invention_time = models.IntegerField()
    invention_materials = models.JSONField(null=True, blank=True, default=list)
    invention_products = models.JSONField(null=True, blank=True, default=list)
    invention_skills = models.JSONField(null=True, blank=True, default=list)
