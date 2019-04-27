"""
Test file for visonic grps server implemented at run_server.py.
This tests check the complete flow opening a socket and communicating
with the server and checking the results.
The configuration to use by the server will be the PROD one, for that
reason you should change the configuration if wanna avoid to corrupt
your data on the db with the tests.
"""
import pytest
import socket
import time


@pytest.mark.e2e
def test_server_reply_and_process_a_request(prod_config):

    # Connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((prod_config['HOST'], int(prod_config['PORT'])))

    # Send the data
    data = 'Test data sent from a e2e test. If you see this, you can safely remove it.'
    len_sent = s.send(data.encode('utf-8'))

    # Receive a response
    response = s.recv(len_sent).decode('utf-8')

    # Clean up
    s.close()

    # Checks
    assert data == response, "[ERROR] The response returned by the server is not equals than the request sent."

    time.sleep(2) # wait a bit before to check the db in order to let the server finish the db tasks

    assert prod_config['DB_CLIENT'].events.count_documents({"raw_request": data}) == 1, 'A new event was expected to be saved at the db containing the request.'

    # In order to try to not corrupt data on the db, we delete that new created document
    prod_config['DB_CLIENT'].events.delete_one({"raw_request": data})
