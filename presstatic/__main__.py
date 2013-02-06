#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import SimpleHTTPServer
import SocketServer

from clint.textui import colored, puts, indent

from presstatic import help
from presstatic.builders import SiteBuilder
from presstatic.storage import s3


def http_server_on_dir(host, port, dir):
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    os.chdir(dir)
    httpd = SocketServer.TCPServer((host, int(port)), Handler)

    with indent(4, quote='>>'):
        puts(colored.green("Serving {path}".format(path=dir)))
        puts(colored.yellow("@ {host}:{port} ".format(host=host, port=port)))
    httpd.serve_forever()


def main():
    cli_parser = argparse.ArgumentParser(prog='presstatic')
    cli_parser.add_argument('-http',
                            metavar='HOST:PORT',
                            help="creates an HTTP Server with <directory> as root dir.")
    cli_parser.add_argument('-s3',
                            help="deploy on the specified S3 bucket.",
                            metavar='bucket')
    cli_parser.add_argument('directory',
                            help='directory containing the static website.')

    cli_args = cli_parser.parse_args()

    if cli_args.http:
        host, port = cli_args.http.split(':')
        http_server_on_dir(host, port, cli_args.directory)
    elif cli_args.s3:
        site_builder = SiteBuilder(cli_args.directory)
        site_builder.build()
        s3.S3Storage(cli_args.s3).store(site_builder.output_path)
        puts(help.s3_setup(bucket=cli_args.s3))

if __name__ == '__main__':
    main()
