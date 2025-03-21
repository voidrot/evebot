from django.db import models


class SchoolMap(models.Model):
    id = models.IntegerField(primary_key=True)
    school_id = models.IntegerField()
    solar_system_id = models.IntegerField()
