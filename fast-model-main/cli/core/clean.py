import subprocess
import sys
from pathlib import Path

import yaml
from typer import Typer

clean_app = Typer()


def clean_for_darwin(config: dict):

    pgdata = config["db"]["pgdata"]
    subprocess.run(["pg_ctl", "-D", pgdata, "stop"])
    subprocess.run(["rm", "-rf", pgdata])


def clean_for_win32(config: dict):
    raise NotImplementedError()


def _clean(config: dict):

    platform = sys.platform

    if platform == "darwin":
        clean_for_darwin(config)

    elif platform == "win32":
        clean_for_win32(config)

    else:
        raise ValueError(f"unsupported platform {sys.platform}")


@clean_app.callback()
def clean(config: Path):
    with open(config, "r") as f:
        config = yaml.load(f, yaml.Loader)

    _clean(config)
