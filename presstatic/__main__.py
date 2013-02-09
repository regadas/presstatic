#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import signal
import argparse
import logging

from clint.textui import colored, puts, indent

from presstatic import help
from presstatic.builder import SiteBuilder
from presstatic.storage import s3
from presstatic.http import HttpServer
from presstatic.watcher import Watcher


http_server = None
watcher = None

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def signal_handler(signal, frame):
    puts('You pressed Ctrl+C!')

    if http_server:
        http_server.stop()
    if watcher:
        watcher.stop()

    sys.exit(0)


def main():
    global http_server, watcher

    cli_parser = argparse.ArgumentParser(prog='presstatic')
    cli_parser.add_argument('-output',
                            help="relative directory for the generated files.",
                            default='public')
    cli_parser.add_argument('-http',
                            metavar='HOST:PORT',
                            help="creates an HTTP Server with <directory> as root dir.")
    cli_parser.add_argument('-s3',
                            help="deploy on the specified S3 bucket.",
                            metavar='bucket')
    cli_parser.add_argument('directory',
                            help='directory containing the static website.')

    cli_args = cli_parser.parse_args()

    site_builder = SiteBuilder(cli_args.directory, output=cli_args.output)
    site_builder.build()

    if cli_args.http:
        host, port = cli_args.http.split(':')
        root_dir = os.path.join(cli_args.directory, cli_args.output)

        signal.signal(signal.SIGINT, signal_handler)

        http_server = HttpServer(host, port, root_dir)
        http_server.start()

        watcher = Watcher(site_builder)
        watcher.start()

        with indent(4, quote='>>'):
            puts(colored.green("Serving {path}".format(path=root_dir)))
            puts(colored.yellow("@ {host}:{port} ".format(host=host, port=port)))

        signal.pause()

    elif cli_args.s3:
        s3.S3Storage(cli_args.s3).store(site_builder.output_path)
        puts(help.s3_setup(bucket=cli_args.s3))


if __name__ == '__main__':
    main()
