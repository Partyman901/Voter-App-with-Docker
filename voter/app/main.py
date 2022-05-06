# main.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from .base import Base
from .vote import Vote
import yaml
import logging
import logging.config

main = Blueprint('main', __name__)
DB_ENGINE = create_engine(f"mysql+pymysql://root:Passw0rd!@mysql:3306/enterdata")
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
logger = logging.getLogger('basicLogger')

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/windows', methods=['POST'])
def windows_post():
    logger.info(f"Windows post has started")
    try:
        try:
            session = DB_SESSION()
        except Exception as e:
            logger.error("FAILED TO CONNECT TO MYSQL")
            print(e)
        vote = Vote(windows=1, mac=0)
        session.add(vote)
        session.commit()
        session.close()
        print("Finished sending data")
        logger.info(f"Windows post has finished")
        return render_template('submission.html')
    except Exception as e:
        print(e)
        return render_template('index.html')

@main.route('/mac', methods=['POST'])
def mac_post():
    try:
        try:
            session = DB_SESSION()
        except Exception as e:
            print(e)
        vote = Vote(windows=0, mac=1)
        session.add(vote)
        session.commit()
        session.close()
        print("Finished sending data")
        return render_template('submission.html')
    except Exception as e:
        print(e)
        return render_template('index.html')

