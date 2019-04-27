import os
import configparser

from pymongo import MongoClient

class Mongo_Connector():
    def __init__(self, config_name=None):
        # read the config
        self.config = configparser.ConfigParser()
        self.config.read(os.path.abspath(os.path.join("server_config.ini")))

        assert config_name in self.config.sections(), "[ERROR] The config_name provided '{}' is not valid, the valid ones are: '{}'.".format(config_name, self.config.sections())

        # instantiate and configure the mongo client, and db to use
        mongo_client = MongoClient(self.config[config_name]['DB_URI'])
        self.db = mongo_client[self.config[config_name]['DB_NAME']]

        return

    def save_raw_request(self, raw_data=None):
        assert raw_data, "[ERROR] No raw data provided to save it."
        # save the raw data at the events collection
        self.db.events.insert_one({'raw_request': raw_data})
