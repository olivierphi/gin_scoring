import functools
import http.client
import logging
import time
from typing import TYPE_CHECKING, Literal, NamedTuple, TypedDict

from django.conf import settings

if TYPE_CHECKING:

    class _PicoCssVersion(TypedDict):
        tag: str
        type: Literal["classless", "conditional"]
        color: Literal[
            "amber",
            "blue",
            "cyan",
            "fuchsia",
            "green",
            "grey",
            "indigo",
            "jade",
            "lime",
            "orange",
            "pink",
            "pumpkin",
            "purple",
            "red",
            "sand",
            "slate",
            "violet",
            "yellow",
            "zinc",
        ]


_PICOS_CSS_VERSION: "_PicoCssVersion" = {
    "tag": "v2.0.6",
    "type": "classless",
    "color": "fuchsia",
}

_logger = logging.getLogger(__name__)


class DownloadedAssets(NamedTuple):
    pico_css_filename: str


def download_assets_if_needed() -> DownloadedAssets:
    # Pico CSS stylesheet management:
    download_pico_css_if_needed()
    pico_css_filename = get_pico_css_filename()

    return DownloadedAssets(pico_css_filename=pico_css_filename)


def download_pico_css_if_needed():
    local_copy_filename = get_pico_css_filename()
    local_copy_path = (
        settings.STATIC_DOWNLOADED_ASSETS_DIR / "css" / local_copy_filename
    )

    if local_copy_path.exists():
        return  # all good, we already downloaded it before 😌

    _logger.info(f"Downloading Pico CSS asset: {local_copy_filename}")
    download_start_time = time.monotonic()

    # Ok, let's download the asset!
    # Its URL has the following form:
    # https://raw.githubusercontent.com/picocss/pico/v2.0.6/css/pico.classless.fuchsia.css
    conn = http.client.HTTPSConnection("raw.githubusercontent.com")
    asset_path = f"/picocss/pico/{_PICOS_CSS_VERSION['tag']}/css/pico.{_PICOS_CSS_VERSION['type']}.{_PICOS_CSS_VERSION['color']}.css"
    conn.request("GET", asset_path)
    response = conn.getresponse()
    if response.status != 200:
        raise RuntimeError(
            f"Failed to download the asset: {asset_path}: got status {response.status}, with content: {response.read()}"
        )
    asset_content = response.read()
    local_copy_path.write_bytes(asset_content)

    download_duration = time.monotonic() - download_start_time
    _logger.info(f"Downloaded Pico CSS asset in {download_duration:.2f} seconds")


@functools.cache
def get_pico_css_filename() -> str:
    return ".".join(
        (
            "pico",
            _PICOS_CSS_VERSION["tag"],
            _PICOS_CSS_VERSION["type"],
            _PICOS_CSS_VERSION["color"],
            "css",
        )
    )
