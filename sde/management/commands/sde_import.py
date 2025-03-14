import asyncio
import hashlib
import logging
import shutil
import time
import zipfile
from asyncio import sleep
from pathlib import Path
from pprint import pprint

import environ
import httpx
import yaml
from aiopath import AsyncPath
from django.conf import settings
from django.core.management.base import BaseCommand
from tqdm.asyncio import tqdm
from tqdm.asyncio import trange

from sde.models import Agent
from sde.models import AgentInSpace
from sde.models import Ancestry
from sde.models import AsteroidBelt
from sde.models import Bloodline
from sde.models import Blueprint
from sde.models import Category
from sde.models import Certificate
from sde.models import CharacterAttribute
from sde.models import Constellation
from sde.models import ContrabandType
from sde.models import ControlTowerResource
from sde.models import CorporationActivity
from sde.models import DogmaAttribute
from sde.models import DogmaAttributeCategory
from sde.models import DogmaEffect
from sde.models import Faction
from sde.models import GraphicID
from sde.models import Group
from sde.models import IconID
from sde.models import InvFlag
from sde.models import InvItem
from sde.models import InvName
from sde.models import InvPosition
from sde.models import InvUniqueName
from sde.models import Landmark
from sde.models import MarketGroup
from sde.models import MetaGroup
from sde.models import Moon
from sde.models import NPCCorporation
from sde.models import NPCCorporationDivision
from sde.models import PackagedVolume
from sde.models import Planet
from sde.models import PlanetResource
from sde.models import PlanetSchematic
from sde.models import Race
from sde.models import Region
from sde.models import ResearchAgent
from sde.models import Skin
from sde.models import SkinLicense
from sde.models import SkinMaterial
from sde.models import SolarSystem
from sde.models import SovereigntyUpgrade
from sde.models import Station
from sde.models import StationOperation
from sde.models import StationService
from sde.models import Type
from sde.models import TypeDogma
from sde.models import TypeMaterial

env = environ.Env()
logger = logging.getLogger(__name__)

try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader

    logger.debug("Successfully imported pyyaml CDumper and CLoader.")
except ImportError:
    from yaml import Dumper
    from yaml import Loader

    logger.warning(
        "Failed to import pyyaml CDumper and CLoader, loads and dumps of YAML may take much longer."
    )


class Command(BaseCommand):
    sde_archive_url = (
        "https://eve-static-data-export.s3-eu-west-1.amazonaws.com/tranquility/sde.zip"
    )
    sde_checksum_url = (
        "https://eve-static-data-export.s3-eu-west-1.amazonaws.com/tranquility/checksum"
    )
    sde_workspace = Path("./.sde-workspace")
    sde_zip_file = Path("/tmp/sde.zip")
    sde_current_checksum = Path(sde_workspace / ".checksum")

    # SDE objects
    # holds the ID lookup for items
    sde_types = {}
    # holds the ID / Name lookup for places
    sde_inv_names = {}
    # holds the Item ID and Group ID of unique names
    sde_inv_unique_names = {}

    jobs = {}

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force fresh download and import of the SDE",
        )

    def handle(self, *args, **options):
        logger.debug("check if sde already exists")

        current_checksum = ""
        latest_checksum = self._get_checksum("sde.zip")
        should_download = True

        if self.sde_current_checksum.exists():
            with Path.open(self.sde_current_checksum) as cs:
                current_checksum = cs.read()

        if current_checksum == latest_checksum and not options["force"]:
            logger.info("No changes detected in SDE")
            should_download = False

        if should_download or options["force"]:
            if self.sde_workspace.exists():
                shutil.rmtree(self.sde_workspace)
            if self.sde_zip_file.exists():
                self.sde_zip_file.unlink()

            logger.debug("creating sde workspace")
            self.sde_workspace.mkdir()

            self._download_sde()
            valdi_sde = self._validate_sde_checksum(latest_checksum)
            if valdi_sde:
                self._extract_sde_archive()
            else:
                logger.error("Failed to extract sde checksum")
                return

        logger.info("starting SDE loading to database")
        self.load_sde_to_database()

    def _get_checksum(self, checksum_name="sde.zip") -> str:
        r = httpx.get(self.sde_checksum_url)
        cs = r.content.decode("utf-8")
        for line in cs.splitlines():
            cs_combo = line.split()
            if cs_combo[1] == checksum_name:
                return cs_combo[0]
        return ""

    def _download_sde(self):
        logger.debug("Downloading SDE archive")
        chunk_size = 1 * 1024**2
        if self.sde_zip_file.exists():
            self.sde_zip_file.unlink()
        with (
            httpx.stream("GET", self.sde_archive_url) as r,
            self.sde_zip_file.open("wb") as f,
        ):
            for chunk in r.iter_bytes(chunk_size=chunk_size):
                f.write(chunk)
        logger.info(f"SDE archive downloaded to {self.sde_zip_file}")

    def _extract_sde_archive(self):
        logger.debug("Extracting SDE archive")
        with zipfile.ZipFile(self.sde_zip_file) as z:
            z.extractall(path=self.sde_workspace)
        logger.info(f"SDE archive extracted to {self.sde_workspace}")

    def _validate_sde_checksum(self, valid_checksum: str) -> bool:
        logger.debug("validating SDE checksum")
        logger.info(f"Validating SDE checksum for {valid_checksum}")
        md5_hash = hashlib.md5(usedforsecurity=False)
        with zipfile.ZipFile(self.sde_zip_file, "r", zipfile.ZIP_DEFLATED) as z:
            file_name = z.namelist()
            for f in file_name:
                md5_hash.update(z.read(f))

        checksum = md5_hash.hexdigest()
        if checksum != valid_checksum:
            logger.error(
                f"SDE checksum failed - got {checksum}, expected {valid_checksum}"
            )
            return False
        else:
            logger.info(f"SDE checksum passed for {valid_checksum}")
            with self.sde_current_checksum.open("w") as cs:
                cs.write(checksum)
            return True

    def _load_yaml(self, p: Path):
        logger.debug(f"parsing yaml file at {str(p.absolute().resolve())}")
        with p.open("r") as t:
            return yaml.load(t.read(), Loader=Loader)

    def load_sde_to_database(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._load_async_tasks())
        logger.info("Finished loading SDE to database")

    async def _log_job_status(self):
        while not all(job.done() for job in self.jobs.values()):
            output = f"""
                Loading InvFlags: {"In Progress" if not self.jobs["inv_flags"].done() else "Done"}
                Loading InvItems: {"In Progress" if not self.jobs["inv_items"].done() else "Done"}
            """
            print(output, end="\r")
            await sleep(1)

    # def _load_types(self):
    #     # logger.debug("loading fsd types")
    #     return self._load_yaml(self.sde_workspace / "fsd" / "types.yaml")

    # def _load_inv_names(self):
    #     # logger.debug("loading bsd invNames")
    #     inv_names = self._load_yaml(self.sde_workspace / "bsd" / "invNames.yaml")
    #     inv_names_obj = {}
    #     for i in inv_names:
    #         inv_names_obj[i["itemID"]] = i["itemName"]
    #     return inv_names_obj

    # def _load_inv_unique_names(self):
    #     # logger.debug("loading bsd invUniqueNames")
    #     uniq_names = self._load_yaml(self.sde_workspace / "bsd" / "invUniqueNames.yaml")
    #     uniq_names_obj = {}
    #     for i in uniq_names:
    #         uniq_names_obj[i["itemID"]] = {
    #             "group_id": i["groupID"],
    #             "name": i["itemName"],
    #         }
    #     return uniq_names_obj

    async def _load_async_tasks(self):
        start = time.monotonic()
        await self._load_agents()
        await self._load_inv_flags()
        await self._load_inv_items()
        await self._load_inv_names()
        await self._load_inv_positions()
        await self._load_inv_unique_names()
        await self._load_sta_stations()
        await self._load_ancestries()
        await self._load_bloodlines()
        await self._load_blueprints()
        await self._load_categories()
        await self._load_certificates()
        await self._load_character_attributes()
        await self._load_contraband_types()
        await self._load_control_tower_resources()
        await self._load_corporation_activity()
        await self._load_dogma_attribute_categories()
        await self._load_dogma_attributes()
        await self._load_dogma_effects()
        await self._load_factions()
        await self._load_graphic_ids()
        await self._load_groups()
        await self._load_icon_ids()
        await self._load_landmarks()
        await self._load_market_groups()
        await self._load_meta_groups()
        await self._load_npc_corporations()
        await self._load_npc_corporation_divisions()
        await self._load_planet_resources()
        await self._load_planet_schematics()
        await self._load_races()
        await self._load_research_agents()
        await self._load_skin_licenses()
        await self._load_skin_materials()
        await self._load_skins()
        await self._load_sovereignty_upgrades()
        await self._load_station_operations()
        await self._load_station_services()
        await self._load_type_dogma()
        await self._load_type_materials()
        await self._load_types()



        logger.info(
            f"Finished loading SDE to database in {time.monotonic() - start:.2f} seconds"
        )

    async def _load_agents(self):
        pass

    async def _load_inv_flags(self):
        logger.info("Loading invFlags data to model")
        inv_flags = self._load_yaml(self.sde_workspace / "bsd" / "invFlags.yaml")
        async with asyncio.TaskGroup() as tg:
            for i in inv_flags:
                inv_flag = InvFlag(
                    id=i["flagID"],
                    flag_name=i["flagName"],
                    flag_text=i["flagText"],
                    order_id=i["orderID"],
                )
                tg.create_task(inv_flag.asave())
        logger.info("Finished loading invFlags data to model")

    async def _load_inv_items(self):
        logger.info("Loading invItems data to model")
        inv_items = self._load_yaml(self.sde_workspace / "bsd" / "invItems.yaml")
        async with asyncio.TaskGroup() as tg:
            for i in inv_items:
                inv_item = InvItem(
                    id=i["itemID"],
                    location_id=i.get("locationID", None),
                    owner_id=i["ownerID"],
                    quantity=i["quantity"],
                    type_id=i["typeID"],
                )
                tg.create_task(inv_item.asave())
        logger.info("Finished loading invItems data to model")

    async def _load_inv_names(self):
        logger.info("Loading invNames data to model")
        inv_names = self._load_yaml(self.sde_workspace / "bsd" / "invNames.yaml")
        async with asyncio.TaskGroup() as tg:
            for i in inv_names:
                inv_name = InvName(
                    id=i["itemID"],
                    item_name=i["itemName"],
                )
                tg.create_task(inv_name.asave())
        logger.info("Finished loading invNames data to model")

    async def _load_inv_positions(self):
        logger.info("Loading invPositions data to model")
        inv_positions = self._load_yaml(
            self.sde_workspace / "bsd" / "invPositions.yaml"
        )
        async with asyncio.TaskGroup() as tg:
            for i in inv_positions:
                inv_position = InvPosition(
                    id=i["itemID"],
                    pitch=i.get("pitch", None),
                    roll=i.get("roll", None),
                    yaw=i.get("yaw", None),
                    x=i["x"],
                    y=i["y"],
                    z=i["z"],
                )
                tg.create_task(inv_position.asave())
        logger.info("Finished loading invPositions data to model")

    async def _load_inv_unique_names(self):
        logger.info("Loading invUniqueNames data to model")
        inv_unique_names = self._load_yaml(
            self.sde_workspace / "bsd" / "invUniqueNames.yaml"
        )
        async with asyncio.TaskGroup() as tg:
            for i in inv_unique_names:
                inv_unique_name = InvUniqueName(
                    id=i["itemID"],
                    group_id=i["groupID"],
                    item_name=i["itemName"],
                )
                tg.create_task(inv_unique_name.asave())
        logger.info("Finished loading invUniqueNames data to model")

    async def _load_sta_stations(self):
        logger.info("Loading staStations data to model")
        sta_stations = self._load_yaml(self.sde_workspace / "bsd" / "staStations.yaml")
        async with asyncio.TaskGroup() as tg:
            for i in sta_stations:
                sta_station = Station(
                    id=i["stationID"],
                    station_name=i["stationName"],
                    station_type_id=i["stationTypeID"],
                    solar_system_id=i["solarSystemID"],
                    constellation_id=i["constellationID"],
                    region_id=i["regionID"],
                    corporation_id=i["corporationID"],
                    docking_cost_per_volume=i["dockingCostPerVolume"],
                    max_ship_volume_dockable=i["maxShipVolumeDockable"],
                    office_rental_cost=i["officeRentalCost"],
                    operation_id=i["operationID"],
                    reprocessing_efficiency=i["reprocessingEfficiency"],
                    reprocessing_hangar_flag=i["reprocessingHangarFlag"],
                    reprocessing_stations_take=i["reprocessingStationsTake"],
                    security=i["security"],
                    x=i["x"],
                    y=i["y"],
                    z=i["z"],
                )
                tg.create_task(sta_station.asave())
        logger.info("Finished loading staStations data to model")

    async def _load_agents(self):
        logger.info("Loading agents data to model")
        agents = self._load_yaml(self.sde_workspace / "fsd" / "agents.yaml")
        async with asyncio.TaskGroup() as tg:
            for k, v in agents.items():
                agent = Agent(
                    id=k,
                    agent_type_id=v["agentTypeID"],
                    corporation_id=v["corporationID"],
                    division_id=v["divisionID"],
                    is_locator=v["isLocator"],
                    level=v["level"],
                    location_id=v["locationID"],
                )
                tg.create_task(agent.asave())
        logger.info("Finished loading agents data to model")

    async def _load_agents_in_space(self):
        logger.info("Loading agents in space data to model")
        agents_in_space = self._load_yaml(
            self.sde_workspace / "fsd" / "agentsInSpace.yaml"
        )
        async with asyncio.TaskGroup() as tg:
            for k, v in agents_in_space.items():
                agent_in_space = AgentInSpace(
                    id=k,
                    dungeon_id=v["dungeonID"],
                    solar_system_id=v["solarSystemID"],
                    spawn_point_id=v["spawnPointID"],
                    type_id=v["typeID"],
                )
                tg.create_task(agent_in_space.asave())
        logger.info("Finished loading agents in space data to model")

    async def _load_ancestries(self):
        logger.info("Loading ancestries data to model")
        ancestries = self._load_yaml(self.sde_workspace / "fsd" / "ancestries.yaml")
        async with asyncio.TaskGroup() as tg:
            for k, v in ancestries.items():
                ancestry = Ancestry(
                    id=k,
                    bloodline_id=v["bloodlineID"],
                    charisma=v["charisma"],
                    description_id=v["descriptionID"],
                    icon_id=v.get("iconID", None),
                    intelligence=v["intelligence"],
                    memory=v["memory"],
                    name_id=v["nameID"],
                    perception=v["perception"],
                    short_description=v.get("shortDescription", None),
                    willpower=v["willpower"],
                )
                tg.create_task(ancestry.asave())
        logger.info("Finished loading ancestries data to model")

    async def _load_bloodlines(self):
        logger.info("Loading bloodlines data to model")
        bloodlines = self._load_yaml(self.sde_workspace / "fsd" / "bloodlines.yaml")
        async with asyncio.TaskGroup() as tg:
            for k, v in bloodlines.items():
                bloodline = Bloodline(
                    id=k,
                    charisma=v["charisma"],
                    corporation_id=v["corporationID"],
                    description_id=v["descriptionID"],
                    icon_id=v.get("iconID", None),
                    intelligence=v["intelligence"],
                    memory=v["memory"],
                    name_id=v["nameID"],
                    perception=v["perception"],
                    race_id=v["raceID"],
                    willpower=v["willpower"],
                )

                tg.create_task(bloodline.asave())
        logger.info("Finished loading bloodlines data to model")

    async def _load_blueprints(self):
        logger.info("Loading blueprints data to model")
        blueprints = self._load_yaml(self.sde_workspace / "fsd" / "blueprints.yaml")
        async with asyncio.TaskGroup() as tg:
            for k, v in blueprints.items():
                blueprint = Blueprint(
                    id=k,
                    activities=v["activities"],
                    blueprint_type_id=v["blueprintTypeID"],
                    max_production_limit=v["maxProductionLimit"],
                )
                tg.create_task(blueprint.asave())
        logger.info("Finished loading blueprints data to model")

    async def _load_categories(self):
        logger.info("Loading categories data to model")
        categories = self._load_yaml(self.sde_workspace / "fsd" / "categories.yaml")
        async with asyncio.TaskGroup() as tg:
            for k, v in categories.items():
                category = Category(
                    id=k,
                    name=v["name"],
                    published=v["published"],
                    icon_id=v.get("iconID", None),
                )
                tg.create_task(category.asave())
        logger.info("Finished loading categories data to model")

    async def _load_certificates(self):
        logger.info("Loading certificates data to model")
        certificates = self._load_yaml(self.sde_workspace / "fsd" / "certificates.yaml")
        async with asyncio.TaskGroup() as tg:
            for k, v in certificates.items():
                certificate = Certificate(
                    id=k,
                    description=v["description"],
                    group_id=v["groupID"],
                    name=v["name"],
                    recommended_for=v.get("recommendedFor", None),
                    skill_types=v["skillTypes"],
                )
                tg.create_task(certificate.asave())
        logger.info("Finished loading certificates data to model")

    async def _load_character_attributes(self):
        logger.info("Loading character attributes data to model")
        character_attributes = self._load_yaml(
            self.sde_workspace / "fsd" / "characterAttributes.yaml"
        )
        async with asyncio.TaskGroup() as tg:
            for k, v in character_attributes.items():
                character_attribute = CharacterAttribute(
                    id=k,
                    name_id=v["nameID"],
                    description=v["description"],
                    notes=v["notes"],
                    icon_id=v.get("iconID", None),
                    short_description=v["shortDescription"],
                )
                tg.create_task(character_attribute.asave())
        logger.info("Finished loading character attributes data to model")

    async def _load_contraband_types(self):
        logger.info("Loading contraband types data to model")
        contraband_types = self._load_yaml(
            self.sde_workspace / "fsd" / "contrabandTypes.yaml"
        )
        async with asyncio.TaskGroup() as tg:
            for k, v in contraband_types.items():
                contraband_type = ContrabandType(
                    id=k,
                    factions=v["factions"],
                )
                tg.create_task(contraband_type.asave())
        logger.info("Finished loading contraband types data to model")

    async def _load_control_tower_resources(self):
        logger.info("Loading control tower resources data to model")
        control_tower_resources = self._load_yaml(
            self.sde_workspace / "fsd" / "controlTowerResources.yaml"
        )
        async with asyncio.TaskGroup() as tg:
            for k, v in control_tower_resources.items():
                control_tower_resource = ControlTowerResource(
                    id=k,
                    resources=v["resources"],
                )
                tg.create_task(control_tower_resource.asave())
        logger.info("Finished loading control tower resources data to model")

    async def _load_corporation_activity(self):
        logger.info("Loading corporation activity data to model")
        corporation_activities = self._load_yaml(
            self.sde_workspace / "fsd" / "corporationActivities.yaml"
        )
        async with asyncio.TaskGroup() as tg:
            for k, v in corporation_activities.items():
                corporation_activity = CorporationActivity(
                    id=k,
                    name_id=v["nameID"],
                )
                tg.create_task(corporation_activity.asave())
        logger.info("Finished loading corporation activity data to model")

    async def _load_dogma_attribute_categories(self):
        logger.info("Loading dogma attribute categories data to model")
        dogma_attribute_categories = self._load_yaml(
            self.sde_workspace / "fsd" / "dogmaAttributeCategories.yaml"
        )
        async with asyncio.TaskGroup() as tg:
            for k, v in dogma_attribute_categories.items():
                dogma_attribute_category = DogmaAttributeCategory(
                    id=k,
                    name=v["name"],
                    description=v.get("description", None),
                )
                tg.create_task(dogma_attribute_category.asave())
        logger.info("Finished loading dogma attribute categories data to model")

    async def _load_dogma_attributes(self):
        logger.info("Loading dogma attributes data to model")
        dogma_attributes = self._load_yaml(
            self.sde_workspace / "fsd" / "dogmaAttributes.yaml"
        )
        async with asyncio.TaskGroup() as tg:
            for k, v in dogma_attributes.items():
                dogma_attribute = DogmaAttribute(
                    id=k,
                    category_id=v.get("categoryID", None),
                    data_type=v["dataType"],
                    default_value=v["defaultValue"],
                    description=v.get("description", None),
                    high_is_good=v["highIsGood"],
                    name=v["name"],
                    published=v["published"],
                    stackable=v["stackable"],
                    display_name_id=v.get("displayNameID", None),
                    icon_id=v.get("iconID", None),
                    tooltip_description_id=v.get("tooltipDescriptionID", None),
                    tooltip_title_id=v.get("tooltipTitleID", None),
                    unit_id=v.get("unitID", None),
                    charge_recharge_time_id=v.get("chargeRechargeTimeID", None),
                    max_attribute_id=v.get("maxAttributeID", None),
                    min_attribute_id=v.get("minAttributeID", None),
                    display_when_zero=v.get("displayWhenZero", None),
                )
                tg.create_task(dogma_attribute.asave())
        logger.info("Finished loading dogma attributes data to model")

    async def _load_dogma_effects(self):
        logger.info("Loading dogma effects data to model")
        dogma_effects = self._load_yaml(
            self.sde_workspace / "fsd" / "dogmaEffects.yaml"
        )
        async with asyncio.TaskGroup() as tg:
            for k, v in dogma_effects.items():
                dogma_effect = DogmaEffect(
                    id=k,
                    disallow_auto_repeat=v["disallowAutoRepeat"],
                    discharge_attribute_id=v.get("dischargeAttributeID", None),
                    duration_attribute_id=v.get("durationAttributeID", None),
                    effect_category=v["effectCategory"],
                    effect_id=v["effectID"],
                    effect_name=v["effectName"],
                    electronic_chance=v["electronicChance"],
                    guid=v.get("guid", None),
                    is_assistance=v["isAssistance"],
                    is_offensive=v["isOffensive"],
                    is_warp_safe=v["isWarpSafe"],
                    propulsion_chance=v["propulsionChance"],
                    published=v["published"],
                    range_chance=v["rangeChance"],
                    distribution=v.get("distribution", None),
                    falloff_attribute_id=v.get("falloffAttributeID", None),
                    range_attribute_id=v.get("rangeAttributeID", None),
                    tracking_speed_attribute_id=v.get("trackingSpeedAttributeID", None),
                    description_id=v.get("descriptionID", None),
                    display_name_id=v.get("displayNameID", None),
                    icon_id=v.get("iconID", None),
                    modifier_info=v.get("modifierInfo", None),
                    sfx_name=v.get("sfxName", None),
                    npc_usage_chance_attribute_id=v.get(
                        "npcUsageChanceAttributeID", None
                    ),
                    npc_activation_chance_attribute_id=v.get(
                        "npcActivationChanceAttributeID", None
                    ),
                    fitting_usage_chance_attribute_id=v.get(
                        "fittingUsageChanceAttributeID", None
                    ),
                    resistance_attribute_id=v.get("resistanceAttributeID", None),
                )
                tg.create_task(dogma_effect.asave())
        logger.info("Finished loading dogma effects data to model")

    async def _load_factions(self):
        logger.info("Loading factions data to model")
        factions = self._load_yaml(self.sde_workspace / "fsd" / "factions.yaml")
        async with asyncio.TaskGroup() as tg:
            for k, v in factions.items():
                faction = Faction(
                    id=k,
                    name_id=v["nameID"],
                    description_id=v.get("descriptionID", None),
                    icon_id=v.get("iconID", None),
                    corporation_id=v.get("corporationID", None),
                    flat_logo=v.get("flatLogo", None),
                    flat_logo_with_name=v.get("flatLogoWithName", None),
                    member_races=v.get("memberRaces", None),
                    militia_corporation_id=v.get("militiaCorporationID", None),
                    short_description_id=v.get("shortDescriptionID", None),
                    size_factor=v.get("sizeFactor", None),
                    solar_system_id=v.get("solarSystemID", None),
                    unique_name=v.get("uniqueName", None),
                )
                tg.create_task(faction.asave())
        logger.info("Finished loading factions data to model")

    async def _load_graphic_ids(self):
        logger.info("Loading graphic ids data to model")
        graphic_ids = self._load_yaml(self.sde_workspace / "fsd" / "graphicIDs.yaml")
        async with asyncio.TaskGroup() as tg:
            for k, v in graphic_ids.items():
                graphic_id = GraphicID(
                    id=k,
                    description=v.get("description", None),
                    graphic_file=v.get("graphicFile", None),
                    icon_info=v.get("iconInfo", None),
                    sof_faction_name=v.get("sofFactionName", None),
                    sof_hull_name=v.get("sofHullName", None),
                    sof_race_name=v.get("sofRaceName", None),
                    sof_layout=v.get("sofLayout", None),
                )
                tg.create_task(graphic_id.asave())
        logger.info("Finished loading graphic ids data to model")

    async def _load_groups(self):
        logger.info("Loading groups data to model")
        groups = self._load_yaml(self.sde_workspace / "fsd" / "groups.yaml")
        async with asyncio.TaskGroup() as tg:
            for k, v in groups.items():
                group = Group(
                    id=k,
                    anchorable=v["anchorable"],
                    anchored=v["anchored"],
                    category_id=v["categoryID"],
                    fittable_non_singleton=v["fittableNonSingleton"],
                    name=v["name"],
                    published=v["published"],
                    use_base_price=v["useBasePrice"],
                    icon_id=v.get("iconID", None),
                )
                tg.create_task(group.asave())
        logger.info("Finished loading groups data to model")

    async def _load_icon_ids(self):
        logger.info("Loading icon ids data to model")
        icon_ids = self._load_yaml(self.sde_workspace / "fsd" / "iconIDs.yaml")
        async with asyncio.TaskGroup() as tg:
            for k, v in icon_ids.items():
                icon_id = IconID(
                    id=k,
                    description=v.get("description", None),
                    icon_file=v.get("iconFile", None),
                    obsolete=v.get("obsolete", None),
                )
                tg.create_task(icon_id.asave())
        logger.info("Finished loading icon ids data to model")

    async def _load_landmarks(self):
        logger.info("Loading landmarks data to model")
        landmarks = self._load_yaml(
            self.sde_workspace / "universe" / "landmarks" / "landmarks.yaml"
        )
        async with asyncio.TaskGroup() as tg:
            for k, v in landmarks.items():
                landmark = Landmark(
                    id=k,
                    description_id=v["descriptionID"],
                    landmark_name_id=v["landmarkNameID"],
                    position=v["position"],
                )
                tg.create_task(landmark.asave())
        logger.info("Finished loading landmarks data to model")

    async def _load_market_groups(self):
        logger.info("Loading market groups data to model")
        market_groups = self._load_yaml(
            self.sde_workspace / "fsd" / "marketGroups.yaml"
        )
        async with asyncio.TaskGroup() as tg:
            for k, v in market_groups.items():
                market_group = MarketGroup(
                    id=k,
                    description_id=v.get("descriptionID", None),
                    has_types=v["hasTypes"],
                    icon_id=v.get("iconID", None),
                    name_id=v["nameID"],
                    parent_group_id=v.get("parentGroupID", None),
                )
                tg.create_task(market_group.asave())
        logger.info("Finished loading market groups data to model")

    async def _load_meta_groups(self):
        logger.info("Loading meta groups data to model")
        meta_groups = self._load_yaml(self.sde_workspace / "fsd" / "metaGroups.yaml")
        async with asyncio.TaskGroup() as tg:
            for k, v in meta_groups.items():
                meta_group = MetaGroup(
                    id=k,
                    color=v.get("color", None),
                    name_id=v["nameID"],
                    icon_id=v.get("iconID", None),
                    icon_suffix=v.get("iconSuffix", None),
                    description_id=v.get("descriptionID", None),
                )
                tg.create_task(meta_group.asave())
        logger.info("Finished loading meta groups data to model")

    async def _load_npc_corporations(self):
        logger.info("Loading NPC corporations data to model")
        npc_corporations = self._load_yaml(
            self.sde_workspace / "fsd" / "npcCorporations.yaml"
        )
        async with asyncio.TaskGroup() as tg:
            for k, v in npc_corporations.items():
                npc_corporation = NPCCorporation(
                    id=k,
                    ceo_id=v.get("ceoID", None),
                    deleted=v["deleted"],
                    description_id=v.get("descriptionID", None),
                    extent=v["extent"],
                    has_player_personnel_manager=v["hasPlayerPersonnelManager"],
                    initial_price=v["initialPrice"],
                    member_limit=v["memberLimit"],
                    min_security=v["minSecurity"],
                    minimum_join_standing=v["minimumJoinStanding"],
                    name_id=v["nameID"],
                    public_shares=v["publicShares"],
                    send_char_termination_message=v["sendCharTerminationMessage"],
                    shares=v["shares"],
                    size=v["size"],
                    station_id=v.get("stationID", None),
                    tax_rate=v["taxRate"],
                    ticker_name=v["tickerName"],
                    unique_name=v["uniqueName"],
                    allowed_member_races=v.get("allowedMemberRaces", None),
                    corporation_trades=v.get("corporationTrades", None),
                    divisions=v.get("divisions", None),
                    enemy_id=v.get("enemyID", None),
                    faction_id=v.get("factionID", None),
                    friend_id=v.get("friendID", None),
                    icon_id=v.get("iconID", None),
                    investors=v.get("investors", None),
                    lp_offer_tables=v.get("lpOfferTables", None),
                    main_activity_id=v.get("mainActivityID", None),
                    race_id=v.get("raceID", None),
                    size_factor=v.get("sizeFactor", None),
                    solar_system_id=v.get("solarSystemID", None),
                    exchange_rates=v.get("exchangeRates", None),
                    secondary_activity_id=v.get("secondaryActivityID", None),
                    url=v.get("url", None),
                )
                tg.create_task(npc_corporation.asave())
        logger.info("Finished loading NPC corporations data to model")

    async def _load_npc_corporation_divisions(self):
        logger.info("Loading NPC corporation divisions data to model")
        npc_corporation_divisions = self._load_yaml(
            self.sde_workspace / "fsd" / "npcCorporationDivisions.yaml"
        )
        async with asyncio.TaskGroup() as tg:
            for k, v in npc_corporation_divisions.items():
                npc_corporation_division = NPCCorporationDivision(
                    id=k,
                    name_id=v["nameID"],
                    description_id=v.get("descriptionID", None),
                    description=v.get("description", None),
                    internal_name=v.get("internalName", None),
                    leader_type_name_id=v.get("leaderTypeNameID", None),
                )
                tg.create_task(npc_corporation_division.asave())
        logger.info("Finished loading NPC corporation divisions data to model")

    async def _load_planet_resources(self):
        logger.info("Loading planet resources data to model")
        planet_resources = self._load_yaml(
            self.sde_workspace / "fsd" / "planetResources.yaml"
        )
        async with asyncio.TaskGroup() as tg:
            for k, v in planet_resources.items():
                planet_resource = PlanetResource(
                    id=k,
                    power=v.get("power", None),
                    workforce=v.get("workforce", None),
                    cycle_minutes=v.get("cycle_minutes", None),
                    harvest_silo_max=v.get("harvest_silo_max", None),
                    maturation_cycle_minutes=v.get("maturation_cycle_minutes", None),
                    maturation_percent=v.get("maturation_percent", None),
                    mature_silo_max=v.get("mature_silo_max", None),
                    reagent_harvest_amount=v.get("reagent_harvest_amount", None),
                    reagent_type_id=v.get("reagent_type_id", None),
                )
                tg.create_task(planet_resource.asave())

    async def _load_planet_schematics(self):
        logger.info("Loading planet schematics data to model")
        planet_schematics = self._load_yaml(
            self.sde_workspace / "fsd" / "planetSchematics.yaml"
        )
        async with asyncio.TaskGroup() as tg:
            for k, v in planet_schematics.items():
                planet_schematic = PlanetSchematic(
                    id=k,
                    cycle_time=v["cycleTime"],
                    name_id=v["nameID"],
                    pins=v["pins"],
                    types=v["types"],
                )
                tg.create_task(planet_schematic.asave())
        logger.info("Finished loading planet schematics data to model")

    async def _load_races(self):
        logger.info("Loading races data to model")
        races = self._load_yaml(self.sde_workspace / "fsd" / "races.yaml")
        async with asyncio.TaskGroup() as tg:
            for k, v in races.items():
                race = Race(
                    id=k,
                    description_id=v.get("descriptionID", None),
                    icon_id=v.get("iconID", None),
                    name_id=v["nameID"],
                    ship_type_id=v.get("shipTypeID", None),
                    skills=v.get("skills", None),
                )
                tg.create_task(race.asave())
        logger.info("Finished loading race data to model")

    async def _load_research_agents(self):
        logger.info("Loading research agents data to model")
        research_agents = self._load_yaml(
            self.sde_workspace / "fsd" / "researchAgents.yaml"
        )
        async with asyncio.TaskGroup() as tg:
            for k, v in research_agents.items():
                research_agent = ResearchAgent(
                    id=k,
                    skills=v["skills"],
                )
                tg.create_task(research_agent.asave())
        logger.info("Finished loading research agents data to model")

    async def _load_skin_licenses(self):
        logger.info("Loading skin licenses data to model")
        skin_licenses = self._load_yaml(
            self.sde_workspace / "fsd" / "skinLicenses.yaml"
        )
        async with asyncio.TaskGroup() as tg:
            for k, v in skin_licenses.items():
                skin_license = SkinLicense(
                    id=k,
                    duration=v["duration"],
                    license_type_id=v["licenseTypeID"],
                    skin_id=v["skinID"],
                    is_single_use=v.get("isSingleUse", None),
                )
                tg.create_task(skin_license.asave())
        logger.info("Finished loading skin licenses data to model")

    async def _load_skin_materials(self):
        logger.info("Loading skin materials data to model")
        skin_materials = self._load_yaml(
            self.sde_workspace / "fsd" / "skinMaterials.yaml"
        )
        async with asyncio.TaskGroup() as tg:
            for k, v in skin_materials.items():
                skin_material = SkinMaterial(
                    id=k,
                    display_name_id=v["displayNameID"],
                    material_set_id=v["materialSetID"],
                    skin_material_id=v["skinMaterialID"],
                )
                tg.create_task(skin_material.asave())
        logger.info("Finished loading skin materials data to model")

    async def _load_skins(self):
        logger.info("Loading skins data to model")
        skins = self._load_yaml(self.sde_workspace / "fsd" / "skins.yaml")
        async with asyncio.TaskGroup() as tg:
            for k, v in skins.items():
                skin = Skin(
                    id=k,
                    allow_ccpdevs=v["allowCCPDevs"],
                    internal_name=v["internalName"],
                    skin_id=v["skinID"],
                    skin_material_id=v["skinMaterialID"],
                    types=v["types"],
                    visible_serenity=v["visibleSerenity"],
                    visible_tranquility=v["visibleTranquility"],
                    is_structure_skin=v.get("isStructureSkin", None),
                    skin_description=v.get("skinDescription", None),
                )
                tg.create_task(skin.asave())
        logger.info("Finished loading skins data to model")

    async def _load_sovereignty_upgrades(self):
        logger.info("Loading sovereignty upgrades data to model")
        sovereignty_upgrades = self._load_yaml(
            self.sde_workspace / "fsd" / "sovereigntyUpgrades.yaml"
        )
        async with asyncio.TaskGroup() as tg:
            for k, v in sovereignty_upgrades.items():
                sovereignty_upgrade = SovereigntyUpgrade(
                    id=k,
                    fuel_hourly_upkeep=v.get("fuel_hourly_upkeep", None),
                    fuel_startup_cost=v.get("fuel_startup_cost", None),
                    fuel_type_id=v.get("fuel_type_id", None),
                    mutually_exclusive_group=v["mutually_exclusive_group"],
                    power_allocation=v["power_allocation"],
                    workforce_allocation=v["workforce_allocation"],
                )
                tg.create_task(sovereignty_upgrade.asave())
        logger.info("Finished loading sovereignty upgrades data to model")

    async def _load_station_operations(self):
        logger.info("Loading station operations data to model")
        station_operations = self._load_yaml(
            self.sde_workspace / "fsd" / "stationOperations.yaml"
        )
        async with asyncio.TaskGroup() as tg:
            for k, v in station_operations.items():
                station_operation = StationOperation(
                    id=k,
                    activity_id=v["activityID"],
                    border=v["border"],
                    corridor=v["corridor"],
                    description_id=v.get("descriptionID", None),
                    fringe=v["fringe"],
                    hub=v["hub"],
                    manufacturing_factor=v["manufacturingFactor"],
                    operation_name_id=v["operationNameID"],
                    ratio=v["ratio"],
                    research_factor=v["researchFactor"],
                    services=v["services"],
                    station_types=v.get("stationTypes", None),
                )
                tg.create_task(station_operation.asave())
        logger.info("Finished loading station operations data to model")

    async def _load_station_operations(self):
        logger.info("Loading station operations data to model")
        station_operations = self._load_yaml(
            self.sde_workspace / "fsd" / "stationOperations.yaml"
        )
        async with asyncio.TaskGroup() as tg:
            for k, v in station_operations.items():
                station_operation = StationOperation(
                    id=k,
                    activity_id=v["activityID"],
                    border=v["border"],
                    corridor=v["corridor"],
                    description_id=v.get("descriptionID", None),
                    fringe=v["fringe"],
                    hub=v["hub"],
                    manufacturing_factor=v["manufacturingFactor"],
                    operation_name_id=v["operationNameID"],
                    ratio=v["ratio"],
                    research_factor=v["researchFactor"],
                    services=v["services"],
                    station_types=v.get("stationTypes", None),
                )
                tg.create_task(station_operation.asave())
        logger.info("Finished loading station operations data to model")

    async def _load_station_services(self):
        logger.info("Loading station services data to model")
        station_services = self._load_yaml(
            self.sde_workspace / "fsd" / "stationServices.yaml"
        )
        async with asyncio.TaskGroup() as tg:
            for k, v in station_services.items():
                station_service = StationService(
                    id=k,
                    service_name_id=v["serviceNameID"],
                    description_id=v["descriptionID"],
                )
                tg.create_task(station_service.asave())
        logger.info("Finished loading station services data to model")

    async def _load_type_dogma(self):
        logger.info("Loading type dogma data to model")
        type_dogma = self._load_yaml(self.sde_workspace / "fsd" / "typeDogma.yaml")
        async with asyncio.TaskGroup() as tg:
            for k, v in type_dogma.items():
                type_dogma = TypeDogma(
                    id=k,
                    dogma_attributes=v["dogmaAttributes"],
                    dogma_effects=v["dogmaEffects"],
                )
                tg.create_task(type_dogma.asave())
        logger.info("Finished loading type dogma data to model")

    async def _load_type_materials(self):
        logger.info("Loading type materials data to model")
        type_materials = self._load_yaml(self.sde_workspace / "fsd" / "typeMaterials.yaml")
        async with asyncio.TaskGroup() as tg:
            for k, v in type_materials.items():
                type_material = TypeMaterial(
                    id=k,
                    materials=v["materials"],
                )
                tg.create_task(type_material.asave())
        logger.info("Finished loading type materials data to model")

    async def _load_types(self):
        logger.info("Loading types data to model")
        types = self._load_yaml(self.sde_workspace / "fsd" / "types.yaml")
        async with asyncio.TaskGroup() as tg:
            for k, v in types.items():
                type_ = Type(
                    id=k,
                    group_id=v["groupID"],
                    mass=v.get("mass", None),
                    name=v["name"],
                    portion_size=v["portionSize"],
                    published=v["published"],
                    volume=v.get("volume", None),
                    radius=v.get("radius", None),
                    description=v.get("description", None),
                    graphic_id=v.get("graphicID", None),
                    sound_id=v.get("soundID", None),
                    icon_id=v.get("iconID", None),
                    race_id=v.get("raceID", None),
                    sof_faction_name = v.get("sofFactionName", None),
                    base_price=v.get("basePrice", None),
                    market_group_id=v.get("marketGroupID", None),
                    capacity=v.get("capacity", None),
                    meta_group_id=v.get("metaGroupID", None),
                    variation_parent_type_id=v.get("variationParentTypeID", None),
                    faction_id=v.get("factionID", None),
                    masteries=v.get("masteries", None),
                    traits=v.get("traits", None),
                    sof_material_set_id=v.get("sofMaterialSetID", None),
                )
                tg.create_task(type_.asave())
        logger.info("Finished loading types data to model")


    # async def _load_solar_system(self):
    #     pass
