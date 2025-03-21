from django.db import models


class NPCCorporation(models.Model):
    id = models.IntegerField(primary_key=True)
    ceo_id = models.IntegerField(default=None, null=True, blank=True)
    deleted = models.BooleanField()
    has_player_personnel_manager = models.BooleanField()
    initial_price = models.IntegerField()
    member_limit = models.IntegerField()
    min_security = models.FloatField()
    minimum_join_standing = models.IntegerField()
    public_shares = models.IntegerField()
    send_char_termination_message = models.BooleanField()
    shares = models.BigIntegerField()
    station_id = models.IntegerField(default=None, null=True, blank=True)
    tax_rate = models.FloatField()
    unique_name = models.BooleanField()
    enemy_id = models.IntegerField(default=None, null=True, blank=True)
    faction_id = models.IntegerField(default=None, null=True, blank=True)
    friend_id = models.IntegerField(default=None, null=True, blank=True)
    icon_id = models.IntegerField(default=None, null=True, blank=True)
    main_activity_id = models.IntegerField(default=None, null=True, blank=True)
    race_id = models.IntegerField(default=None, null=True, blank=True)
    size_factor = models.FloatField(default=None, null=True, blank=True)
    solar_system_id = models.IntegerField(default=None, null=True, blank=True)
    secondary_activity_id = models.IntegerField(default=None, null=True, blank=True)
    description_id = models.JSONField(default=dict, null=True, blank=True)
    extent = models.TextField()
    name_id = models.JSONField()
    size = models.TextField()
    ticker_name = models.TextField()
    allowed_member_races = models.JSONField(default=list, null=True, blank=True)
    corporation_trades = models.JSONField(default=dict, null=True, blank=True)
    divisions = models.JSONField(default=dict, null=True, blank=True)
    investors = models.JSONField(default=dict, null=True, blank=True)
    lp_offer_tables = models.JSONField(default=list, null=True, blank=True)
    exchange_rates = models.JSONField(default=dict, null=True, blank=True)
    url = models.TextField(null=True, default=None)  # noqa: DJ001

    def __str__(self):
        return f"{self.name_id['en']}"
