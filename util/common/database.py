"""
Database and Database Path Management
"""
import os
from os import path
import json
import subprocess


def get_oxide_root():
    """Return the absolute path to the Project Oxide repo root"""
    return path.abspath(path.join(__file__, "../../../"))


def get_db_root():
    """
    Return the path containing the Project Oxide database
    This is database/ in the repo, unless the `PRJOXIDE_DB` environment
    variable is set to another value.
    """
    if "PRJOXIDE_DB" in os.environ and os.environ["PRJOXIDE_DB"] != "":
        return os.environ["PRJOXIDE_DB"]
    else:
        return path.join(get_oxide_root(), "database")


def get_db_subdir(family = None, device = None, package = None):
    """
    Return the DB subdirectory corresponding to a family, device and
    package (all if applicable), creating it if it doesn't already
    exist.
    """
    subdir = get_db_root()
    dparts = [family, device, package]
    for dpart in dparts:
        if dpart is None:
            break
        subdir = path.join(subdir, dpart)
        if not path.exists(subdir):
            os.mkdir(subdir)
    return subdir


def get_tilegrid(family, device):
    """
    Return the deserialised tilegrid for a family, device
    """
    tgjson = path.join(get_db_subdir(family, device), "tilegrid.json")
    with open(tgjson, "r") as f:
        return json.load(f)


def get_devices():
    """
    Return the deserialised content of devices.json
    """
    djson = path.join(get_db_root(), "devices.json")
    with open(djson, "r") as f:
        return json.load(f)


def get_db_commit():
    return subprocess.getoutput('git -C "{}" rev-parse HEAD'.format(get_db_root()))
