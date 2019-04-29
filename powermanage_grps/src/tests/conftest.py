import pytest
from os import environ
from pymongo import MongoClient
from configparser import ConfigParser


def get_appconfig():
    app_config = ConfigParser()
    app_config.read(environ['CONF_FILE'])
    return app_config


def mongo_client(uri=None, db_name=None):
    assert uri, '[ERROR] The uri is mandantory.'
    assert db_name, '[ERROR] The db_name is mandatory.'

    mongo_client = MongoClient(uri, serverSelectionTimeoutMS=3000)

    db = mongo_client[db_name]
    return db


@pytest.fixture
def prod_config():
    app_config = get_appconfig()
    config = {}
    config['HOST'] = app_config['PROD']['HOST']
    config['PORT'] = app_config['PROD']['PORT']
    config['DB_URI'] = app_config['PROD']['DB_URI']
    config['DB_NAME'] = app_config['PROD']['DB_NAME']

    print('[INFO] Getting the Mongo Client for the PROD configuration.')
    config['DB_CLIENT'] = mongo_client(config['DB_URI'], config['DB_NAME'])
    return config


@pytest.fixture
def test_config():
    app_config = get_appconfig()
    config = {}
    # config['HOST'] = app_config['TEST']['HOST']
    # config['PORT'] = app_config['TEST']['PORT']
    config['DB_URI'] = app_config['TEST']['DB_URI']
    config['DB_NAME'] = app_config['TEST']['DB_NAME']

    print('[INFO] Getting the Mongo Client for the TEST configuration.')
    config['DB_CLIENT'] = mongo_client(config['DB_URI'], config['DB_NAME'])
    return config
