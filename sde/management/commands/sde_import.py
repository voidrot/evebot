import asyncio
import hashlib
import logging
import shutil
import zipfile
from asyncio import sleep
from pathlib import Path
import environ
import httpx
import yaml
from django.core.management.base import BaseCommand
from django.conf import settings

env = environ.Env()
logger = logging.getLogger(__name__)

try:
    from yaml import CLoader as Loader, CDumper as Dumper

    logger.debug("Successfully imported pyyaml CDumper and CLoader.")
except ImportError:
    from yaml import Loader, Dumper

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
        self._load_lookups()
        loop.run_until_complete(self._load_async_tasks())
        logger.info("Finished loading SDE to database")

    def _load_lookups(self):
        logger.debug("loading static lookups")
        self.sde_types = self._load_types()
        self.sde_inv_names = self._load_inv_names()
        self.sde_inv_unique_names = self._load_inv_unique_names()

    def _load_types(self):
        logger.debug("loading fsd types")
        return self._load_yaml(self.sde_workspace / "fsd" / "types.yaml")

    def _load_inv_names(self):
        logger.debug("loading bsd invNames")
        inv_names = self._load_yaml(self.sde_workspace / "bsd" / "invNames.yaml")
        inv_names_obj = {}
        for i in inv_names:
            inv_names_obj[i["itemID"]] = i["itemName"]
        return inv_names_obj

    def _load_inv_unique_names(self):
        logger.debug("loading bsd invUniqueNames")
        uniq_names = self._load_yaml(self.sde_workspace / "bsd" / "invUniqueNames.yaml")
        uniq_names_obj = {}
        for i in uniq_names:
            uniq_names_obj[i["itemID"]] = {
                "group_id": i["groupID"],
                "name": i["itemName"],
            }
        return uniq_names_obj


    async def _load_async_tasks(self):
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self._load_agents())

    async def _load_agents(self):
        pass
