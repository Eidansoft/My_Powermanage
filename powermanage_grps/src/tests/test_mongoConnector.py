"""
Test file for the MongoConnector for the project
"""

import pytest

from mongo_connector import Mongo_Connector


def get_mongo_connector():
    return Mongo_Connector('TEST')

@pytest.mark.unittests
def test_persist_raw_request_at_mongo(test_config):
    # clear the collection
    test_config['DB_CLIENT'].events.drop()

    # run the method to test
    connector = get_mongo_connector()
    data = "This is the raw request"
    connector.save_raw_request(data)

    # check
    assert test_config['DB_CLIENT'].events.count_documents({"raw_request": data}) == 1, 'A new event was expected to be saved at the db containing the request.'
