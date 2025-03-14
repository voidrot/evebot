# Generated by Django 5.1.6 on 2025-03-09 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Agent",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("agent_type_id", models.IntegerField()),
                ("corporation_id", models.IntegerField()),
                ("division_id", models.IntegerField()),
                ("is_locator", models.BooleanField()),
                ("level", models.IntegerField()),
                ("location_id", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="AgentInSpace",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("dungeon_id", models.IntegerField()),
                ("solar_system_id", models.IntegerField()),
                ("spawn_point_id", models.IntegerField()),
                ("type_id", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Ancestry",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("bloodline_id", models.IntegerField()),
                ("charisma", models.IntegerField()),
                ("description_id", models.JSONField()),
                ("icon_id", models.IntegerField(blank=True, default=None, null=True)),
                ("intelligence", models.IntegerField()),
                ("memory", models.IntegerField()),
                ("name_id", models.JSONField()),
                ("perception", models.IntegerField()),
                ("short_description", models.TextField(default=None)),
                ("willpower", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="AsteroidBelt",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("planet_id", models.IntegerField()),
                ("solar_system_id", models.IntegerField()),
                ("region_id", models.IntegerField()),
                ("constellation_id", models.IntegerField()),
                ("position", models.JSONField(default=dict)),
                ("statistics", models.JSONField(default=dict)),
                ("type_id", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Bloodline",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("charisma", models.IntegerField()),
                ("corporation_id", models.IntegerField()),
                ("description_id", models.JSONField()),
                ("icon_id", models.IntegerField(blank=True, default=None, null=True)),
                ("intelligence", models.IntegerField()),
                ("memory", models.IntegerField()),
                ("name_id", models.JSONField()),
                ("perception", models.IntegerField()),
                ("race_id", models.IntegerField()),
                ("willpower", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Blueprint",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("activities", models.JSONField(default=dict)),
                ("blueprint_type_id", models.IntegerField()),
                ("max_production_limit", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.JSONField()),
                ("published", models.BooleanField()),
                ("icon_id", models.IntegerField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Certificate",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("description", models.TextField()),
                ("group_id", models.IntegerField()),
                ("name", models.TextField()),
                (
                    "recommended_for",
                    models.JSONField(blank=True, default=list, null=True),
                ),
                ("skill_types", models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name="CharacterAttribute",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("description", models.TextField()),
                ("icon_id", models.IntegerField()),
                ("name_id", models.JSONField()),
                ("notes", models.TextField()),
                ("short_description", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Constellation",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("center", models.JSONField()),
                ("constellation_id", models.IntegerField()),
                ("max", models.JSONField()),
                ("min", models.JSONField()),
                ("name_id", models.IntegerField()),
                ("radius", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="ContrabandType",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("factions", models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name="ControlTowerResource",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("resources", models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name="CorporationActivity",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("name_id", models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name="DogmaAttribute",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("attribute_id", models.IntegerField()),
                (
                    "category_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                ("data_type", models.IntegerField()),
                ("default_value", models.FloatField()),
                ("description", models.TextField(default=None)),
                ("high_is_good", models.BooleanField()),
                ("name", models.TextField()),
                ("published", models.BooleanField()),
                ("stackable", models.BooleanField()),
                (
                    "display_name_id",
                    models.JSONField(blank=True, default=dict, null=True),
                ),
                ("icon_id", models.IntegerField(blank=True, default=None, null=True)),
                (
                    "tooltip_description_id",
                    models.JSONField(blank=True, default=dict, null=True),
                ),
                (
                    "tooltip_title_id",
                    models.JSONField(blank=True, default=dict, null=True),
                ),
                ("unit_id", models.IntegerField(blank=True, default=None, null=True)),
                (
                    "charge_recharge_time_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                (
                    "max_attribute_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                (
                    "min_attribute_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                (
                    "display_when_zero",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DogmaAttributeCategory",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("description", models.TextField(default=None)),
                ("name", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="DogmaEffect",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("disallow_auto_repeat", models.BooleanField()),
                (
                    "discharge_attribute_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                (
                    "duration_attribute_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                ("effect_category", models.IntegerField()),
                ("effect_id", models.IntegerField()),
                ("effect_name", models.TextField()),
                ("electronic_chance", models.BooleanField()),
                ("guid", models.TextField(default=None)),
                ("is_assistance", models.BooleanField()),
                ("is_offensive", models.BooleanField()),
                ("is_warp_safe", models.BooleanField()),
                ("propulsion_chance", models.BooleanField()),
                ("published", models.BooleanField()),
                ("range_chance", models.BooleanField()),
                (
                    "distribution",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                (
                    "falloff_attribute_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                (
                    "range_attribute_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                (
                    "tracking_speed_attribute_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                (
                    "description_id",
                    models.JSONField(blank=True, default=dict, null=True),
                ),
                (
                    "display_name_id",
                    models.JSONField(blank=True, default=dict, null=True),
                ),
                ("icon_id", models.IntegerField(blank=True, default=None, null=True)),
                (
                    "modifier_info",
                    models.JSONField(blank=True, default=list, null=True),
                ),
                ("sfx_name", models.TextField(default=None)),
                (
                    "npc_usage_chance_attribute_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                (
                    "npc_activation_chance_attribute_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                (
                    "fitting_usage_chance_attribute_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                (
                    "resistance_attribute_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Faction",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                (
                    "corporation_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                ("description_id", models.JSONField()),
                ("flat_logo", models.TextField(default=None)),
                ("flat_logo_with_name", models.TextField(default=None)),
                ("icon_id", models.IntegerField()),
                ("member_races", models.JSONField()),
                (
                    "militia_corporation_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                ("name_id", models.JSONField()),
                (
                    "short_description_id",
                    models.JSONField(blank=True, default=dict, null=True),
                ),
                ("size_factor", models.FloatField()),
                ("solar_system_id", models.IntegerField()),
                ("unique_name", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="GraphicID",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("description", models.TextField(default=None)),
                ("graphic_file", models.TextField(default=None)),
                ("icon_info", models.JSONField(blank=True, default=dict, null=True)),
                ("sof_faction_name", models.TextField(default=None)),
                ("sof_hull_name", models.TextField(default=None)),
                ("sof_race_name", models.TextField(default=None)),
                ("sof_layout", models.JSONField(blank=True, default=list, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Group",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("anchorable", models.BooleanField()),
                ("anchored", models.BooleanField()),
                ("category_id", models.IntegerField()),
                ("fittable_non_singleton", models.BooleanField()),
                ("name", models.JSONField()),
                ("published", models.BooleanField()),
                ("use_base_price", models.BooleanField()),
                ("icon_id", models.IntegerField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="IconID",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("description", models.TextField(default=None)),
                ("icon_file", models.TextField()),
                ("obsolete", models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="InvFlag",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("flag_name", models.TextField()),
                ("flag_text", models.TextField()),
                ("order_id", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="InvItem",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("flag_id", models.IntegerField()),
                ("item_id", models.IntegerField()),
                ("location_id", models.IntegerField()),
                ("owner_id", models.IntegerField()),
                ("quantity", models.IntegerField()),
                ("type_id", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="InvName",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("item_id", models.IntegerField()),
                ("item_name", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="InvPosition",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("item_id", models.IntegerField()),
                ("pitch", models.FloatField(blank=True, default=None, null=True)),
                ("roll", models.FloatField(blank=True, default=None, null=True)),
                ("x", models.FloatField()),
                ("y", models.FloatField()),
                ("yaw", models.FloatField(blank=True, default=None, null=True)),
                ("z", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="InvUniqueName",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("group_id", models.IntegerField()),
                ("item_id", models.IntegerField()),
                ("item_name", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Landmark",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("description_id", models.IntegerField()),
                ("landmark_name_id", models.IntegerField()),
                ("position", models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name="MarketGroup",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                (
                    "description_id",
                    models.JSONField(blank=True, default=dict, null=True),
                ),
                ("has_types", models.BooleanField()),
                ("icon_id", models.IntegerField(blank=True, default=None, null=True)),
                ("name_id", models.JSONField()),
                (
                    "parent_group_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MetaGroup",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("color", models.JSONField(blank=True, default=list, null=True)),
                ("name_id", models.JSONField()),
                ("icon_id", models.IntegerField(blank=True, default=None, null=True)),
                ("icon_suffix", models.TextField(default=None)),
                (
                    "description_id",
                    models.JSONField(blank=True, default=dict, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Moon",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("planet_id", models.IntegerField()),
                ("solar_system_id", models.IntegerField()),
                ("region_id", models.IntegerField()),
                ("constellation_id", models.IntegerField()),
                ("celestial_index", models.IntegerField()),
                ("moon_attributes", models.JSONField(default=dict)),
                ("position", models.JSONField(default=dict)),
                ("radius", models.IntegerField()),
                ("statistics", models.JSONField(default=dict)),
                ("type_id", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="NPCCorporation",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("ceo_id", models.IntegerField(blank=True, default=None, null=True)),
                ("deleted", models.BooleanField()),
                (
                    "description_id",
                    models.JSONField(blank=True, default=dict, null=True),
                ),
                ("extent", models.TextField()),
                ("has_player_personnel_manager", models.BooleanField()),
                ("initial_price", models.IntegerField()),
                ("member_limit", models.IntegerField()),
                ("min_security", models.FloatField()),
                ("minimum_join_standing", models.IntegerField()),
                ("name_id", models.JSONField()),
                ("public_shares", models.IntegerField()),
                ("send_char_termination_message", models.BooleanField()),
                ("shares", models.IntegerField()),
                ("size", models.TextField()),
                (
                    "station_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                ("tax_rate", models.FloatField()),
                ("ticker_name", models.TextField()),
                ("unique_name", models.BooleanField()),
                (
                    "allowed_member_races",
                    models.JSONField(blank=True, default=list, null=True),
                ),
                (
                    "corporation_trades",
                    models.JSONField(blank=True, default=dict, null=True),
                ),
                ("divisions", models.JSONField(blank=True, default=dict, null=True)),
                ("enemy_id", models.IntegerField(blank=True, default=None, null=True)),
                (
                    "faction_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                ("friend_id", models.IntegerField(blank=True, default=None, null=True)),
                ("icon_id", models.IntegerField(blank=True, default=None, null=True)),
                ("investors", models.JSONField(blank=True, default=dict, null=True)),
                (
                    "lp_offer_tables",
                    models.JSONField(blank=True, default=list, null=True),
                ),
                (
                    "main_activity_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                ("race_id", models.IntegerField(blank=True, default=None, null=True)),
                ("size_factor", models.FloatField(blank=True, default=None, null=True)),
                (
                    "solar_system_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                (
                    "exchange_rates",
                    models.JSONField(blank=True, default=dict, null=True),
                ),
                (
                    "secondary_activity_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                ("url", models.TextField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name="NPCCorporationDivision",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("description", models.TextField(default=None)),
                ("internal_name", models.TextField()),
                ("leader_type_name_id", models.JSONField()),
                ("name_id", models.JSONField()),
                (
                    "description_id",
                    models.JSONField(blank=True, default=dict, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PackagedVolume",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("group_name", models.TextField()),
                ("packaged_volume", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Planet",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("celestial_index", models.IntegerField()),
                ("planet_attributes", models.JSONField(default=dict)),
                ("position", models.JSONField(default=dict)),
                ("radius", models.IntegerField()),
                ("statistics", models.JSONField(default=dict)),
                ("type_id", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="PlanetResource",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("power", models.IntegerField(blank=True, default=None, null=True)),
                ("workforce", models.IntegerField(blank=True, default=None, null=True)),
                (
                    "cycle_minutes",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                (
                    "harvest_silo_max",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                (
                    "maturation_cycle_minutes",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                (
                    "maturation_percent",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                (
                    "mature_silo_max",
                    models.FloatField(blank=True, default=None, null=True),
                ),
                (
                    "reagent_harvest_amount",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                (
                    "reagent_type_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PlanetSchematic",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("cycle_time", models.IntegerField()),
                ("name_id", models.JSONField()),
                ("pins", models.JSONField()),
                ("types", models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name="Race",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                (
                    "description_id",
                    models.JSONField(blank=True, default=dict, null=True),
                ),
                ("icon_id", models.IntegerField(blank=True, default=None, null=True)),
                ("name_id", models.JSONField()),
                (
                    "ship_type_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                ("skills", models.JSONField(blank=True, default=dict, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Region",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("center", models.JSONField()),
                ("description_id", models.IntegerField()),
                ("faction_id", models.IntegerField()),
                ("max", models.JSONField()),
                ("min", models.JSONField()),
                ("name_id", models.IntegerField()),
                ("nebula", models.IntegerField()),
                ("region_id", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="ResearchAgent",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("skills", models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name="Skin",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("allow_ccpdevs", models.BooleanField()),
                ("internal_name", models.TextField()),
                ("skin_id", models.IntegerField()),
                ("skin_material_id", models.IntegerField()),
                ("types", models.JSONField()),
                ("visible_serenity", models.BooleanField()),
                ("visible_tranquility", models.BooleanField()),
                (
                    "is_structure_skin",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
                ("skin_description", models.TextField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name="SkinLicense",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("duration", models.IntegerField()),
                ("license_type_id", models.IntegerField()),
                ("skin_id", models.IntegerField()),
                (
                    "is_single_use",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SkinMaterial",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("display_name_id", models.IntegerField()),
                ("material_set_id", models.IntegerField()),
                ("skin_material_id", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="SolarSystem",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("border", models.BooleanField()),
                ("center", models.JSONField()),
                ("corridor", models.BooleanField()),
                ("fringe", models.BooleanField()),
                ("hub", models.BooleanField()),
                ("international", models.BooleanField()),
                ("luminosity", models.FloatField()),
                ("max", models.JSONField()),
                ("min", models.JSONField()),
                ("radius", models.FloatField()),
                ("regional", models.BooleanField()),
                ("security", models.FloatField()),
                ("solar_system_id", models.IntegerField()),
                ("solar_system_name_id", models.IntegerField()),
                ("star_id", models.IntegerField()),
                ("sun_type_id", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="SovereigntyUpgrade",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                (
                    "fuel_hourly_upkeep",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                (
                    "fuel_startup_cost",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                (
                    "fuel_type_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                ("mutually_exclusive_group", models.TextField()),
                ("power_allocation", models.IntegerField()),
                ("workforce_allocation", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Station",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("constellation_id", models.IntegerField()),
                ("corporation_id", models.IntegerField()),
                ("docking_cost_per_volume", models.IntegerField()),
                ("max_ship_volume_dockable", models.IntegerField()),
                ("office_rental_cost", models.IntegerField()),
                ("operation_id", models.IntegerField()),
                ("region_id", models.IntegerField()),
                ("reprocessing_efficiency", models.FloatField()),
                ("reprocessing_hangar_flag", models.IntegerField()),
                ("reprocessing_stations_take", models.FloatField()),
                ("security", models.FloatField()),
                ("solar_system_id", models.IntegerField()),
                ("station_id", models.IntegerField()),
                ("station_name", models.TextField()),
                ("station_type_id", models.IntegerField()),
                ("x", models.FloatField()),
                ("y", models.FloatField()),
                ("z", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="StationOperation",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("activity_id", models.IntegerField()),
                ("border", models.FloatField()),
                ("corridor", models.FloatField()),
                (
                    "description_id",
                    models.JSONField(blank=True, default=dict, null=True),
                ),
                ("fringe", models.FloatField()),
                ("hub", models.FloatField()),
                ("manufacturing_factor", models.FloatField()),
                ("operation_name_id", models.JSONField()),
                ("ratio", models.FloatField()),
                ("research_factor", models.FloatField()),
                ("services", models.JSONField()),
                (
                    "station_types",
                    models.JSONField(blank=True, default=dict, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StationService",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("service_name_id", models.JSONField()),
                (
                    "description_id",
                    models.JSONField(blank=True, default=dict, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Type",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("group_id", models.IntegerField()),
                ("mass", models.FloatField(blank=True, default=None, null=True)),
                ("name", models.JSONField()),
                ("portion_size", models.IntegerField()),
                ("published", models.BooleanField()),
                ("volume", models.FloatField(blank=True, default=None, null=True)),
                ("radius", models.FloatField(blank=True, default=None, null=True)),
                ("description", models.JSONField(blank=True, default=dict, null=True)),
                (
                    "graphic_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                ("sound_id", models.IntegerField(blank=True, default=None, null=True)),
                ("icon_id", models.IntegerField(blank=True, default=None, null=True)),
                ("race_id", models.IntegerField(blank=True, default=None, null=True)),
                ("sof_faction_name", models.TextField(default=None)),
                ("base_price", models.FloatField(blank=True, default=None, null=True)),
                (
                    "market_group_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                ("capacity", models.FloatField(blank=True, default=None, null=True)),
                (
                    "meta_group_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                (
                    "variation_parent_type_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                (
                    "faction_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                ("masteries", models.JSONField(blank=True, default=dict, null=True)),
                ("traits", models.JSONField(blank=True, default=dict, null=True)),
                (
                    "sof_material_set_id",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TypeDogma",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("dogma_attributes", models.JSONField()),
                ("dogma_effects", models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name="TypeMaterial",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("materials", models.JSONField()),
            ],
        ),
    ]
