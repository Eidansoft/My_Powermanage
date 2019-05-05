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

def send_and_get_response(prod_config, request):
    # Connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((prod_config['HOST'], int(prod_config['PORT'])))

    len_sent = s.send(request)

    # Receive a response
    response = s.recv(len_sent)

    # Clean up
    s.close()

    return response


@pytest.mark.e2e
def test_server_reply_and_process_a_request(prod_config):
    # Send the data
    data = 'Test data sent from a e2e test. If you see this, you can safely remove it.'.encode('utf-8')
    response = send_and_get_response(prod_config, data)

    # Checks
    assert data == response, "[ERROR] The response returned by the server is not equals than the request sent."

    time.sleep(2) # wait a bit before to check the db in order to let the server finish the db tasks

    element = prod_config['DB_CLIENT'].events.find_one({"raw_request": data})
    assert element , 'A new event was expected to be saved at the db containing the request.'

    # In order to try to not corrupt data on the db, we delete that new created document
    prod_config['DB_CLIENT'].events.delete_one({"_id": element['_id']})


@pytest.mark.e2e
def test_server_split_properly_the_SEQ(prod_config):
    # Send the data
    data = b'\n\x8b\x82005A"*VIS-OIP"0001R0L0#0A17D6[94EFEBCFA3A6FC8CFC8B4450AA2996F1'
    response = send_and_get_response(prod_config, data)

    # Checks
    assert data == response, "[ERROR] The response returned by the server is not equals than the request sent."

    time.sleep(2) # wait a bit before to check the db in order to let the server finish the db tasks

    element = prod_config['DB_CLIENT'].events.find_one({"raw_request": data})
    assert element , 'A new event was expected to be saved at the db containing the request.'
    assert element['SEQ_str'] == '0001', 'The sequence value was not properly processed.'
    # In order to try to not corrupt data on the db, we delete that new created document
    prod_config['DB_CLIENT'].events.delete_one({"_id": element['_id']})


@pytest.mark.e2e
def test_server_split_properly_the_ID(prod_config):
    # Send the data
    data = b'\n\xb1\x81005A"*VIS-OIP"0014R0L0#0A17D6[592A2F1303F2E4F14E2925C265659E5154'
    response = send_and_get_response(prod_config, data)

    # Checks
    assert data == response, "[ERROR] The response returned by the server is not equals than the request sent."

    time.sleep(2) # wait a bit before to check the db in order to let the server finish the db tasks

    element = prod_config['DB_CLIENT'].events.find_one({"raw_request": data})
    assert element , 'A new event was expected to be saved at the db containing the request.'
    assert element['ID_str'] == '*VIS-OIP', 'The ID value was not properly processed.'
    # In order to try to not corrupt data on the db, we delete that new created document
    prod_config['DB_CLIENT'].events.delete_one({"_id": element['_id']})


@pytest.mark.e2e
def test_server_split_properly_the_ENCRYPTED_DATA(prod_config):
    # Send the data
    data = b'\n\xb1\x81005A"*VIS-OIP"0014R0L0#0A17D6[592A2F1303F2E4F14E2925C265659E5154'
    response = send_and_get_response(prod_config, data)

    # Checks
    assert data == response, "[ERROR] The response returned by the server is not equals than the request sent."

    time.sleep(2) # wait a bit before to check the db in order to let the server finish the db tasks

    element = prod_config['DB_CLIENT'].events.find_one({"raw_request": data})
    assert element , 'A new event was expected to be saved at the db containing the request.'
    assert element['ENCRYPTED_ascii'] == b'592A2F1303F2E4F14E2925C265659E5154'
    # In order to try to not corrupt data on the db, we delete that new created document
    prod_config['DB_CLIENT'].events.delete_one({"_id": element['_id']})
