from pathlib import Path
import configparser
import os

# Base directory which is the tracker_api folder.
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment in which the code is run.
ENV = os.environ.setdefault("TRACKER_ENV", "development")

# Config of from the environment file.
CNF = configparser.ConfigParser()
CNF.read(BASE_DIR / "resources" / f"{ENV}.ini")

# Run the application in debug mode.
DEBUG = CNF.getboolean("DEFAULT", "DEBUG")

# Database settings.
SQLALCHEMY_DATABASE_URI = CNF.get("DEFAULT", "SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = CNF.getboolean(
    "DEFAULT", "SQLALCHEMY_TRACK_MODIFICATIONS"
)
