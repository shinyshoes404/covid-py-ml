import os, platform

# determine the absolute path to the configuration directory
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))


class MlConfig:
    conf_urls = {
        "casecounts" : "https://utahcovidtrack.com/api/case-counts/state-of-utah",
        "testing" : "https://utahcovidtrack.com/api/testing",
        "icu-top16" : "https://utahcovidtrack.com/api/icu/top-16"
    }

    icu_date_offset = 19


class DbConfig:
    # the db file will be located in covid-py-ml/data
    # if the system we are running on is Windows, use back slashes
    if platform.system() == "Windows":
        db_path = os.path.join(CONFIG_DIR, "..\..\..\data\covid_ml.db")
    # otherwise use forward slashes
    else:
        db_path = os.path.join(CONFIG_DIR, "../../../data/covid_ml.db")