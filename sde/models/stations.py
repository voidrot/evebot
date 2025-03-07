from django.db import models


class Station(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=90)
    station_type_id = models.IntegerField()
    constellation_id = models.IntegerField()
    corporation_id = models.IntegerField()
    docking_cost_per_volume = models.IntegerField()
    max_ship_volume_dockable = models.IntegerField()
    office_rental_cost = models.IntegerField()
    operation_id = models.IntegerField()
    region_id = models.IntegerField()
    reprocessing_efficiency = models.FloatField()
    reprocessing_hanger_flag = models.IntegerField()
    reprocessing_stations_take = models.FloatField()
    security = models.FloatField()
    solar_system_id = models.IntegerField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
