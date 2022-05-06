from pstats import Stats
from re import S
import connexion
from connexion import NoContent
import yaml
import logging
import logging.config
import requests
import os
import pymongo
from pymongo import MongoClient
# import dnspython
from base import Base

from apscheduler.schedulers.background import BackgroundScheduler
from stats import Stats
from data import Data

from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')
DB_ENGINE = create_engine(f"mysql+pymysql://root:Passw0rd!@mysql:3306/enterdata")
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,'interval',seconds=app_config['scheduler']['period_sec'])
    sched.start()

def populate_stats():
    """ Periodically update stats """
    logger.info(f"Populate stats has started")
    try:
        try:
            session = DB_SESSION()
        except Exception as e:
            logger.error("FAILED TO CONNECT TO MYSQL")
            print(e)
        data_list = session.query(Data).all()
        data_dicts = []
        for data in data_list:
            data_dicts.append(data.to_dict())
        logger.info(f"Data received! {len(data_dicts)} votes received")

        windows_votes = 0
        for data in data_dicts:
            windows_votes += data["windows"]
        mac_votes = 0
        for data in  data_dicts:
            mac_votes += data["mac"]    

        if len(data_dicts) != 0:
            windows_percent = round((windows_votes / len(data_dicts)) * 100, 2)
            mac_percent = round((mac_votes / len(data_dicts)) * 100, 2)
        else:
            windows_percent = 50
            mac_percent = 50
        print("windows_percent = ", windows_percent)
        print("mac_percent", mac_percent)
        stats = Stats(windows_percent, mac_percent)
        stats_dict = stats.to_dict()
        print(stats_dict)
        session.close()
        try:
            mongo_client = MongoClient("mongodb://root:password@mongodb:27017/")
        except Exception as e:
            print(e)
            logger.error("FAILED TO CONNECT TO MONGODB")
        db_name = mongo_client['getdata']
        collection_name = db_name['getdata']
        collection_name.insert_one(stats_dict)

        logger.info("Finished processing data")
    except Exception as e:
        print(e)
        logger.error("Failed to receive data :(")
    

def get_stats():
    """ Get stats event """
    logger.info("get_stats request has started")
    session = DB_SESSION()
    last_updated = session.query(Stats).order_by(Stats.last_updated.desc()).first()
    if last_updated == None:
        logger.error("Statistics do not exist!")
    data_dict = last_updated.to_dict()
    logger.debug(f"Coverted to dictionary: {data_dict}")
    logger.info("get_stats requests has completed!")
    session.close()

    return data_dict, 200


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)

if __name__== "__main__":
    init_scheduler()
    app.run(port=8100, debug=True)