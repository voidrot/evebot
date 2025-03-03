import asyncio
import logging
from pathlib import Path

import environ
import yaml
from django.core.management.base import BaseCommand
from django.conf import settings

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

env = environ.Env()
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    sde_archive_url = (
        "https://eve-static-data-export.s3-eu-west-1.amazonaws.com/tranquility/sde.zip"
    )
    sde_workspace = Path(
        env.path("SDE_DOWNLOAD_DIR", default=Path(settings.BASE_DIR / "sde-workspace"))
    )
    sde_checksum_url = (
        "https://eve-static-data-export.s3-eu-west-1.amazonaws.com/tranquility/checksum"
    )
    sde_archive = sde_workspace / "sde.zip"
    sde_data = {}

    def handle(self, *args, **options):
        loop = asyncio.get_event_loop()
        logger.info("Importing SDE archive")
        loop.run_until_complete(self.load_sde())
        logger.info("Done Importing SDE archive")

    async def load_sde(self):
        async with asyncio.TaskGroup() as tg:
            inv_flags = tg.create_task(
                self._load_yaml(self.sde_workspace / "bsd" / "invFlags.yaml")
            )
            inv_items = tg.create_task(
                self._load_yaml(self.sde_workspace / "bsd" / "invItems.yaml")
            )
            inv_names = tg.create_task(
                self._load_yaml(self.sde_workspace / "bsd" / "invNames.yaml")
            )
            inv_positions = tg.create_task(
                self._load_yaml(self.sde_workspace / "bsd" / "invPositions.yaml")
            )
            inv_unique_names = tg.create_task(
                self._load_yaml(self.sde_workspace / "bsd" / "invUniqueNames.yaml")
            )
            stations = tg.create_task(
                self._load_yaml(self.sde_workspace / "bsd" / "staStations.yaml")
            )
            agents = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "agents.yaml"))
            agents_in_space = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "agentsInSpace.yaml"))
            ancestries = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "ancestries.yaml"))
            bloodlines = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "bloodlines.yaml"))
            blueprints = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "blueprints.yaml"))
            categories = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "categories.yaml"))
            certificates = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "certificates.yaml"))
            character_attributes = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "characterAttributes.yaml"))
            contraband_types = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "contrabandTypes.yaml"))
            control_tower_resources = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "controlTowerResources.yaml"))
            corporation_activities = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "corporationActivities.yaml"))
            dogma_attribute_categories = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "dogmaAttributeCategories.yaml"))
            dogma_attributes = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "dogmaAttributes.yaml"))
            dogma_effects = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "dogmaEffects.yaml"))
            factions = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "factions.yaml"))
            graphic_ids = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "graphicIDs.yaml"))
            groups = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "groups.yaml"))
            icon_ids = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "iconIDs.yaml"))
            market_groups = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "marketGroups.yaml"))
            meta_groups = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "metaGroups.yaml"))
            npc_corporation_divisions = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "npcCorporationDivisions.yaml"))
            npc_corporations = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "npcCorporations.yaml"))
            planet_resources = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "planetResources.yaml"))
            planet_schematics = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "planetSchematics.yaml"))
            races = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "races.yaml"))
            research_agents = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "researchAgents.yaml"))
            skin_licenses = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "skinLicenses.yaml"))
            skin_materials = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "skinMaterials.yaml"))
            skins = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "skins.yaml"))
            sovereignty_upgrades = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "sovereigntyUpgrades.yaml"))
            station_operations = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "stationOperations.yaml"))
            station_services = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "stationServices.yaml"))
            type_dogma = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "typeDogma.yaml"))
            agents = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "agents.yaml"))
            agents = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "agents.yaml"))
            agents = tg.create_task(self._load_yaml(self.sde_workspace / "fsd" / "agents.yaml"))

        self.sde_data["inv_flags"] = inv_flags.result()
        self.sde_data["inv_items"] = inv_items.result()
        self.sde_data["inv_names"] = inv_names.result()
        self.sde_data["inv_positions"] = inv_positions.result()
        self.sde_data["inv_unique_names"] = inv_unique_names.result()
        self.sde_data["stations"] = stations.result()



    @staticmethod
    async def _load_yaml(path):
        with Path.open(path, "r") as f:
            return yaml.load(f.read(), Loader=Loader)
