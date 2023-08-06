#!/usr/bin/python3

import json

# import threading
import socket

from tornado.httpserver import HTTPServer
from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop
from tornado.web import Application, url  # RequestHandler, StaticFileHandler, Application, url
# import os

# DEBUG = socket.gethostname() == "arch"
DEBUG = False


########################################################################
class Clients(dict):
    """"""

    # ----------------------------------------------------------------------
    def shell(self, client):
        """"""
        return self[client][1]

    # ----------------------------------------------------------------------

    def client(self, client):
        """"""
        return self[client][0]

    # ----------------------------------------------------------------------
    def write_message(self, client, message):
        """"""
        self.client(client).write_message(message)


clients = Clients()


########################################################################
class WSHandler(WebSocketHandler):
    """"""

    # ----------------------------------------------------------------------
    def check_origin(self, origin):
        """"""
        return True

    # ----------------------------------------------------------------------

    def open(self):
        """"""
        self.print_log('tornado_ok')

    # ----------------------------------------------------------------------

    def on_close(self):
        """"""
        if hasattr(self, 'client_id'):
            if DEBUG:
                print("connection closed: {}".format(self.client_id))

            if self.client_id in clients:
                client_g = clients[self.client_id]

                if self in client_g['web']:
                    client_g['web'].remove(self)
                    print('Clossed: web')

                elif self == client_g['device']:
                    client_g['device'] = None
                    print('Clossed: device')
                    for web in client_g['web']:
                        web.write_message({'log': 'Device unlinked', })

    # ----------------------------------------------------------------------

    def print_log(self, message):
        """"""
        try:
            self.write_message({'log': message})
        except Exception as error:
            print(message)
            print(error)
            try:
                self.write_message({'log': error})
            except:
                pass

    # ----------------------------------------------------------------------
    def on_message(self, message):
        """"""
        if message:
            data = json.loads(message)
            getattr(self, 'espresso_{action}'.format(**data))(**data)

    # ----------------------------------------------------------------------
    def espresso_register(self, **kwargs):
        """"""
        id = kwargs['id']
        type = kwargs['type']

        self.client_id = id

        if not id in clients.keys():
            clients[id] = {'device': None,
                           'web': [],
                           }

        if type == 'device':
            clients[id]['device'] = self

            for web in clients[id]['web']:
                web.write_message({'log': 'Device linked', })

        elif type == 'web':
            clients[id]['web'].append(self)

        self.print_log("Registration successful {}:{}".format(id, type))
        if DEBUG:
            print("Registration successful {}:{}".format(id, type))

    # ----------------------------------------------------------------------
    def espresso_stream(self, **kwargs):
        """"""
        id = kwargs['id']
        type = kwargs['type']

        if type == 'web':
            if id in clients:
                if clients[id]['device']:
                    clients[id]['device'].write_message(kwargs['data'])
            else:
                kwargs['bounce'] = True
                for web in clients[id]['web']:
                    web.write_message(kwargs['data'])
        elif type == 'device':
            for web in clients[id]['web']:
                web.write_message(kwargs['data'])


# ----------------------------------------------------------------------
def make_app():

    settings = {
        "debug": DEBUG,
        # "static_path": os.path.join(os.path.dirname(__file__), 'html', 'resources'),
        # 'static_url_prefix': '/static/',
        "xsrf_cookies": False,
    }

    return Application([

        url(r'^/ws', WSHandler),

    ], **settings)


# ----------------------------------------------------------------------
def run():
    """"""

    port = 3200

    print("Pitoncore running on port {}".format(port))
    application = make_app()
    http_server = HTTPServer(application)
    http_server.listen(port)
    IOLoop.instance().start()


if __name__ == '__main__':
    run()
