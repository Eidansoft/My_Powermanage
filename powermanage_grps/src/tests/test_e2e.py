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
from random import choice
from string import ascii_uppercase, digits


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
    data = b'\n\x8b\x82005A"THIS-TEST"0001R0L0#0A17D6[94EFEBCFA3A6FC8CFC8B4450AA2996F1'
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
    data = b'\n\xb1\x81005A"THIS-TEST"0014R0L0#0A17D6[592A2F1303F2E4F14E2925C265659E5154'
    response = send_and_get_response(prod_config, data)

    # Checks
    assert data == response, "[ERROR] The response returned by the server is not equals than the request sent."

    time.sleep(2) # wait a bit before to check the db in order to let the server finish the db tasks

    element = prod_config['DB_CLIENT'].events.find_one({"raw_request": data})
    assert element , 'A new event was expected to be saved at the db containing the request.'
    assert element['ID_str'] == 'THIS-TEST', 'The ID value was not properly processed.'
    # In order to try to not corrupt data on the db, we delete that new created document
    prod_config['DB_CLIENT'].events.delete_one({"_id": element['_id']})


@pytest.mark.e2e
def test_server_split_properly_the_ENCRYPTED_DATA(prod_config):
    # Send the data
    data = b'\n\xb1\x81005A"THIS-TEST"0014R0L0#0A17D6[592A2F1303F2E4F14E2925C265659E5154'
    response = send_and_get_response(prod_config, data)

    # Checks
    assert data == response, "[ERROR] The response returned by the server is not equals than the request sent."

    time.sleep(2) # wait a bit before to check the db in order to let the server finish the db tasks

    element = prod_config['DB_CLIENT'].events.find_one({"raw_request": data})
    assert element , 'A new event was expected to be saved at the db containing the request.'
    assert element['ENCRYPTED_ascii'] == '592A2F1303F2E4F14E2925C265659E5154'
    # In order to try to not corrupt data on the db, we delete that new created document
    prod_config['DB_CLIENT'].events.delete_one({"_id": element['_id']})


@pytest.mark.e2e
def test_server_split_properly_the_L(prod_config):
    # Send the data
    data = b'\n:D009F"THIS-TEST"0002R0L0A17D6#000007[212BBAC067455B0DB64B97FEAC433B06'
    response = send_and_get_response(prod_config, data)

    # Checks
    assert data == response, "[ERROR] The response returned by the server is not equals than the request sent."

    time.sleep(2) # wait a bit before to check the db in order to let the server finish the db tasks

    element = prod_config['DB_CLIENT'].events.find_one({"raw_request": data})
    assert element , 'A new event was expected to be saved at the db containing the request.'
    assert element['L_ascii'] == '0A17D6'
    # In order to try to not corrupt data on the db, we delete that new created document
    prod_config['DB_CLIENT'].events.delete_one({"_id": element['_id']})


@pytest.mark.e2e
def test_the_max_length_set_at_config(prod_config):
    # This test needs a special configuration at the config file setting the BUFFER_SIZE
    # to at least 4096 in order to read all the characters.
    # Send the data
    random_string = ''.join(choice(ascii_uppercase + digits) for i in range(40 - 37))
    data = b'\n\xb1\x81005A"THIS-TEST"0014R0L0#0A17D6[' + random_string.encode('utf-8')
    response = send_and_get_response(prod_config, data)

    # Checks
    assert data == response, "[ERROR] The response returned by the server was expected to be the same than the request. Do you configure the server with the BUFFER_SIZE to be at least 4096 ???."

    time.sleep(2) # wait a bit before to check the db in order to let the server finish the db tasks

    element = prod_config['DB_CLIENT'].events.find_one({"ID_str": 'THIS-TEST'})
    assert element , 'A new event was expected to be saved at the db containing the request but truncating the last element of the request because the buffer limit set to 1024.'

    assert element['ENCRYPTED_ascii'] == random_string
    # In order to try to not corrupt data on the db, we delete that new created document
    prod_config['DB_CLIENT'].events.delete_one({"_id": element['_id']})


@pytest.mark.e2e
def test_server_save_the_client_ip(prod_config):
    # Send the data
    data = b'\n:D009F"THIS-TEST"0002R0L0A17D6#000007[212BBAC067455B0DB64B97FEAC433B06'
    response = send_and_get_response(prod_config, data)

    # Checks
    assert data == response, "[ERROR] The response returned by the server is not equals than the request sent."

    time.sleep(2) # wait a bit before to check the db in order to let the server finish the db tasks

    element = prod_config['DB_CLIENT'].events.find_one({"raw_request": data})
    assert element , 'A new event was expected to be saved at the db containing the request.'
    assert element['request_ip'], 'The client IP was expected to be included at the DB log.'
    # In order to try to not corrupt data on the db, we delete that new created document
    prod_config['DB_CLIENT'].events.delete_one({"_id": element['_id']})
