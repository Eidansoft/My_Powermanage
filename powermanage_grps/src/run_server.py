import logging
import sys
import socketserver as SocketServer
import configparser
from os import environ
from mongo_connector import Mongo_Connector


logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )

class EchoRequestHandler(SocketServer.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('EchoRequestHandler')
        self.logger.debug('__init__')
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def setup(self):
        self.logger.debug('setup')
        return SocketServer.BaseRequestHandler.setup(self)

    def save_raw_request(self, data):
        mongo_client = Mongo_Connector('PROD')
        mongo_client.save_raw_request(data)

    def handle(self):
        self.logger.debug('handle')

        # read the request
        data = self.request.recv(1024).decode('utf-8')

        self.logger.debug('received -> "%s"', data)
        self.logger.debug('responding back -> "%s"', data)

        # Echo the back to the client
        self.request.send(data.encode('utf-8'))

        # save the request for futher analisys
        self.save_raw_request(data)

        return

    def finish(self):
        self.logger.debug('finish')
        return SocketServer.BaseRequestHandler.finish(self)

class EchoServer(SocketServer.TCPServer):

    def __init__(self, server_address, handler_class=EchoRequestHandler):
        self.logger = logging.getLogger('EchoServer')
        self.logger.debug('__init__')
        SocketServer.TCPServer.__init__(self, server_address, handler_class)
        return

    def server_activate(self):
        self.logger.debug('server_activate')
        SocketServer.TCPServer.server_activate(self)
        return

    def serve_forever(self):
        self.logger.debug('serve_forever')
        self.logger.info('waiting for request')
        self.logger.info('Handling requests, press <Ctrl-C> to quit')
        while True:
            self.handle_request()
        return

    def handle_request(self):
        self.logger.debug('handle_request')
        return SocketServer.TCPServer.handle_request(self)

    def verify_request(self, request, client_address):
        self.logger.debug('verify_request(%s, %s)', request, client_address)
        return SocketServer.TCPServer.verify_request(self, request, client_address)

    def process_request(self, request, client_address):
        self.logger.debug('process_request(%s, %s)', request, client_address)
        return SocketServer.TCPServer.process_request(self, request, client_address)

    def server_close(self):
        self.logger.debug('server_close')
        return SocketServer.TCPServer.server_close(self)

    def finish_request(self, request, client_address):
        self.logger.debug('finish_request(%s, %s)', request, client_address)
        return SocketServer.TCPServer.finish_request(self, request, client_address)

    def close_request(self, request_address):
        self.logger.debug('close_request(%s)', request_address)
        return SocketServer.TCPServer.close_request(self, request_address)

if __name__ == '__main__':
    # read the config
    config = configparser.ConfigParser()
    config.read(environ['CONF_FILE'])
    address = (config['PROD']['HOST'], int(config['PROD']['PORT']))
    server = EchoServer(address, EchoRequestHandler)
    # ip, port = server.server_address # find out what port we were given
    logger = logging.getLogger('server')
    logger.info('Server on %s:%s', config['PROD']['HOST'], config['PROD']['PORT'])
    # t = threading.Thread(target=server.serve_forever)
    # t.setDaemon(True) # don't hang on exit
    # t.start()
    server.serve_forever()

    # server.socket.close()
