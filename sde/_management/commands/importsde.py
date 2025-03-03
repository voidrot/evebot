import shutil
import zipfile
from pathlib import Path
from typing import AnyStr
import asyncio
import djclick as click
import environ
import httpx
import yaml
from django.conf import settings
from django.template.defaultfilters import default

# from sde.models import InvFlag
# from sde.models import InvItem
# from sde.models import InvName
# from sde.models import InvPosition
# from sde.models import InvUniqName
# from sde.models import Station

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

env = environ.Env()


SDE_ARCHIVE_URL = (
    "https://eve-static-data-export.s3-eu-west-1.amazonaws.com/tranquility/sde.zip"
)
CHECKSUMS_URL = (
    "https://eve-static-data-export.s3-eu-west-1.amazonaws.com/tranquility/checksum"
)
SDE_WORKSPACE = Path(
    env.path("SDE_DOWNLOAD_DIR", default=Path(settings.BASE_DIR / "sde-workspace"))
)
SDE_ARCHIVE = SDE_WORKSPACE / "sde.zip"


def _load_yaml(stream: AnyStr):
    return yaml.load(stream, Loader=Loader)


def load_file(path: Path):
    with Path.open(path) as f:
        return _load_yaml(f.read())


@click.command()
@click.option("--force", is_flag=True)
@click.option("--bsd", is_flag=True)
@click.option("--fsd", is_flag=True)
@click.option("--universe", is_flag=True)
async def command(force, bsd, fsd, universe):
    """Download and import SDE into database"""

    if SDE_WORKSPACE.exists():
        pass
    else:
        SDE_WORKSPACE.mkdir(parents=True)
    if not SDE_ARCHIVE.exists() or force is True:
        click.secho("Downloading SDE...")
        Path.unlink(SDE_ARCHIVE)
        shutil.rmtree(SDE_WORKSPACE / "bsd")
        shutil.rmtree(SDE_WORKSPACE / "fsd")
        shutil.rmtree(SDE_WORKSPACE / "universe")
        download_sde()

    asyncio.run(import_sde_bsd(bsd, fsd, universe))


def get_sde_checksum() -> str:
    """Discover sde.zip md5 checksum and return it"""
    r = httpx.get(CHECKSUMS_URL)
    cs = r.content.decode()
    for line in cs.splitlines():
        checksum = line.split()
        if checksum[1] == "sde.zip":
            return checksum[0]
    raise Exception("Unable to find sde.zip checksum")  # noqa: EM101, RUF100, TRY002, TRY003


def download_sde():
    with (
        httpx.stream("GET", SDE_ARCHIVE_URL) as r,
        Path.open(SDE_ARCHIVE, "wb") as f,
    ):
        for chunk in r.iter_bytes():
            f.write(chunk)
    with zipfile.ZipFile(SDE_ARCHIVE, "r") as zf:
        zf.extractall(SDE_WORKSPACE)


async def import_sde_bsd(bsd: bool, fsd: bool, universe: bool):
    # import invFlags.yaml  into database
    full_import: bool = bsd is False and fsd is False and universe is False
    print(full_import)

    with asyncio.TaskGroup() as tg:
        inv_flags = tg.create_task(load_file(SDE_WORKSPACE / "bsd" / "invFlags.yaml"))
        inv_items = tg.create_task(load_file(SDE_WORKSPACE / "bsd" / "invItems.yaml"))
        inv_names = tg.create_task(load_file(SDE_WORKSPACE / "bsd" / "invNames.yaml"))
        inv_positions = tg.create_task(
            load_file(SDE_WORKSPACE / "bsd" / "invPositions.yaml")
        )
        inv_unique_names = tg.create_task(
            load_file(SDE_WORKSPACE / "bsd" / "invUniqueNames.yaml")
        )
        stations = tg.create_task(load_file(SDE_WORKSPACE / "bsd" / "staStations.yaml"))

        click.secho("Starting Loading SDE Files...")
    click.secho("Finished Loading SDE Files...")
    # click.secho(flags)

    # if full_import or bsd:
    #     click.secho("Importing invFlags.yaml", fg="green")
    #     with Path.open(SDE_WORKSPACE / "bsd" / "invFlags.yaml", "r") as flags:
    #         r = load_yaml(flags.read())
    #         for i in r:
    #             try:
    #                 # click.secho(i, fg="yellow")
    #                 InvFlag(
    #                     flag_id=i["flagID"],
    #                     name=i["flagName"],
    #                     name_long=i["flagText"],
    #                     order_id=i["orderID"],
    #                 ).save()
    #             except Exception as e:
    #                 click.secho(e, fg="red")
    #     # import invItems.yaml into database
    #     click.secho("Importing invItems.yaml", fg="green")
    #     with Path.open(SDE_WORKSPACE / "bsd" / "invItems.yaml", "r") as items:
    #         r = load_yaml(items.read())
    #         for i in r:
    #             try:
    #                 # click.secho(i, fg="yellow")
    #                 InvItem(
    #                     flag_id=i["flagID"],
    #                     item_id=i["itemID"],
    #                     location_id=i["locationID"],
    #                     owner_id=i["ownerID"],
    #                     quantity=i["quantity"],
    #                     type_id=i["typeID"],
    #                 ).save()
    #             except Exception as e:
    #                 click.secho(e, fg="red")
    #     # import invNames.yaml into database
    #     click.secho("Importing invName.yaml", fg="green")
    #     with Path.open(SDE_WORKSPACE / "bsd" / "invNames.yaml", "r") as names:
    #         r = Loader(names.read())
    #         for i in r:
    #             try:
    #                 click.secho(i, fg="yellow")
    #                 InvName(item_id=i["itemID"], name=i["itemName"]).save()
    #             except Exception as e:
    #                 click.secho(e, fg="red")
    #     # import invPositions.yaml into database
    #     click.secho("Importing invPositions.yaml", fg="green")
    #     with Path.open(SDE_WORKSPACE / "bsd" / "invPositions.yaml", "r") as positions:
    #         r = Loader(positions.read())
    #         for i in r:
    #             try:
    #                 click.secho(i, fg="yellow")
    #                 InvPosition(
    #                     item_id=i["itemID"], x=i["x"], y=i["y"], z=i["z"]
    #                 ).save()
    #             except Exception as e:
    #                 click.secho(e, fg="red")
    #     # import invUniqueNames.yaml into database
    #     click.secho("Importing invUniqueNames.yaml", fg="green")
    #     with Path.open(
    #         SDE_WORKSPACE / "bsd" / "invUniqueNames.yaml", "r"
    #     ) as uniq_names:
    #         r = Loader(uniq_names.read())
    #         for i in r:
    #             try:
    #                 click.secho(i, fg="yellow")
    #                 InvUniqName(
    #                     item_id=i["itemID"], group_id=i["groupID"], name=i["itemName"]
    #                 ).save()
    #             except Exception as e:
    #                 click.secho(e, fg="red")
    #     # import staStations.yaml into database
    #     click.secho("Importing staStations.yaml", fg="green")
    #     with Path.open(SDE_WORKSPACE / "bsd" / "staStations.yaml", "r") as stations:
    #         r = Loader(stations.read())
    #         for i in r:
    #             try:
    #                 click.secho(i, fg="yellow")
    #                 Station(
    #                     station_id=i["stationID"],
    #                     station_name=i["stationName"],
    #                     x=i["x"],
    #                     y=i["y"],
    #                     z=i["z"],
    #                     station_type_id=i["stationTypeID"],
    #                     corporation_id=i["corporationID"],
    #                     solar_system_id=i["solarSystemID"],
    #                     region_id=i["regionID"],
    #                     operation_id=i["operationID"],
    #                     security_rating=i["security"],
    #                     docking_cost_per_volume=i["dockingCostPerVolume"],
    #                     max_ship_volume_dockable=i["maxShipVolumeDockable"],
    #                     office_rental_cost=i["officeRentalCost"],
    #                     reprocessing_efficiency=i["reprocessingEfficiency"],
    #                     reprocessing_stations_take=i["reprocessingStationsTake"],
    #                     reprocessing_hanger_flag=i["reprocessingHangarFlag"],
    #                     constellation_id=i["constellationID"],
    #                 ).save()
    #             except Exception as e:
    #                 click.secho(e, fg="red")
    # import FSD items

    # import Universe items
    ## system paths are REGION / CONSTELLATION / SOLAR SYSTEM NAME / SOLAR SYSTEM DETAILS.yaml
