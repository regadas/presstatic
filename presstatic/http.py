# -*- coding: utf-8 -*-

import os
import SocketServer
import SimpleHTTPServer
from threading import Thread


class HttpServer(object):

    def __init__(self, host, port, root_dir):
        os.chdir(root_dir)

        handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        self.server = SocketServer.TCPServer((host, int(port)), handler, False)
        self.server.allow_reuse_address = True

    def start(self):
        self.server.server_bind()
        self.server.server_activate()

        self.server_thread = Thread(target=self.server.serve_forever)
        self.server_thread.start()

    def stop(self):
        self.server.shutdown()
        self.server_thread.join()
