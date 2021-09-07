import os, platform

# determine the absolute path to the configuration directory
# we will use this to keep track of where our sqlite db file is located
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))


class MlConfig:
    # these are the urls of the api endpoints where we will get our data
    conf_urls = {
        "casecounts" : "https://utahcovidtrack.com/api/case-counts/state-of-utah",
        "testing" : "https://utahcovidtrack.com/api/testing",
        "icu-top16" : "https://utahcovidtrack.com/api/icu/top-16"
    }

    # setting the offset (in days) to move the icu data dates in the data transofrmation process
    # the number will be subtracted from the raw date
    icu_date_offset = 19

    # polynomial degree for our regression model
    poly_degree = 6

    # number of days for smoothing data using moving average
    mv_avg_days = 7

    # number of days before data is stabilized and mature for use with predictions
    data_days_to_mature = 4


class DbConfig:
    # the db file will be located in covid-py-ml/data
    # if the system we are running on is Windows, use back slashes
    if platform.system() == "Windows":
        db_dir = os.path.join(CONFIG_DIR, "..\..\data")
        db_path = os.path.join(db_dir, ".\covid_ml.db")
    # otherwise use forward slashes
    else:
        db_dir = os.path.join(CONFIG_DIR,"../../data")
        db_path = os.path.join(db_dir, "./covid_ml.db")