import configparser
import sys
from datetime import datetime
from os import environ


from pymongo import MongoClient

class Mongo_Connector():
    def __init__(self, config_name=None):
        # read the config
        self.config = configparser.ConfigParser()
        self.config.read(environ['CONF_FILE'])

        assert config_name in self.config.sections(), "[ERROR] The config_name provided '{}' is not valid, the valid ones are: '{}'.".format(config_name, self.config.sections())

        # instantiate and configure the mongo client, and db to use
        mongo_client = MongoClient(self.config[config_name]['DB_URI'], connectTimeoutMS=5000)
        self.db = mongo_client[self.config[config_name]['DB_NAME']]

        return

    def save_raw_request(self, raw_data=None):
        assert raw_data, "[ERROR] No raw data provided to save it."
        # save the raw data at the events collection
        if raw_data[0] == 10:
            # split the request only if the first character is the expected 0x0a
            try:
                res = split_raw_request_into_SIA_fields(raw_data)
            except:
                res = {'error': 'Request split process failed with a "{}" exception.'.format(sys.exc_info()[0])}
        else:
            res = {'error': 'Request does not start with the expected 0x0a character.'}

        res['utc_datetime'] = datetime.utcnow()
        res['raw_request'] = raw_data
        return self.db.events.insert_one(res)


    def split_raw_request_into_SIA_fields(self, raw_data=None):
        elemento = raw_data
        partes = elemento.split(bytes([ord('"')]))
        subpartes2 = partes[2].split(bytes([ord('#')]))
        LF = partes[0][0]
        CRC = []
        for i in range(1, 3):
            CRC.append(partes[0][i])
        LLL = []
        for i in range(3, 7):
            LLL.append(partes[0][i])
        SEQ = []
        for i in range(0, 4):
            SEQ.append(partes[2][i])
        L = subpartes2[0].split(bytes([ord('L')]))[1]
        R = subpartes2[0].split(bytes([ord('L')]))[0].split(bytes([ord('R')]))[1]
        ACCT = subpartes2[1].split(bytes([ord('[')]))[0]
        encrypted_data = subpartes2[1].split(bytes([ord('[')]))[1]

        res = {}
        res['LF_bin'] = LF
        res['CRC_ascii'] = [chr(i) for i in CRC]
        res['0LLL_ascii'] = [chr(i) for i in LLL]
        res['ID_str'] = partes[1].decode('ascii')
        res['ENCRYPTED_bool'] = partes[1].decode('ascii').startswith('*')
        res['SEQ_str'] = ''.join([chr(i) for i in SEQ])
        res['SEQ_int'] = int(''.join([chr(i) for i in SEQ]))
        res['R_bin'] = R
        res['L_bin'] = L
        res['ACCT_bin'] = ACCT
        res['ENCRYPTED_ascii'] = encrypted_data

        return res
