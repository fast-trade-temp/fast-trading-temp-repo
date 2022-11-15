from pathlib import Path
import subprocess
import sys

import yaml
from typer import Typer

setup_app = Typer()


def setup_for_darwin(config: dict):
    subprocess.run(["initdb", "-D", config["db"]["pgdata"]])
    subprocess.run(["pg_ctl", "-D", config["db"]["pgdata"], "start"])

    psql = ["psql", "-d", "postgres", "-c"]

    def create_user(username: str, password: str, dbname: str):
        # fmt: off
        subprocess.run(psql + [f"CREATE DATABASE {dbname};"])
        subprocess.run(psql + [f"CREATE USER {username} WITH ENCRYPTED PASSWORD '{password}';"])
        subprocess.run(psql + [f"GRANT ALL PRIVILEGES ON DATABASE {dbname} TO {username};"])
        # fmt: on

    for user in config["db"]["dbs"]:
        create_user(user["username"], user["password"], user["dbname"])


def setup_for_win32(config: dict):
    raise NotImplementedError()


def _setup(config: dict):

    platform = sys.platform

    if platform == "darwin":
        setup_for_darwin(config)

    elif platform == "win32":
        setup_for_win32(config)

    else:
        raise ValueError(f"unsupported platform {sys.platform}")


@setup_app.callback()
def setup(config: Path):
    with open(config, "r") as f:
        config = yaml.load(f, yaml.Loader)

    _setup(config)
