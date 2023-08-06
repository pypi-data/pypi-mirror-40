#!/usr/bin/env python
from __future__ import print_function
import sys
from collections import namedtuple
import argparse
import routers
from lookups import OnionServiceLookup
import config_handlers
import olib
from functools import partial
from socket import error as socket_error
import msockets as msockets
import custom_exceptions as exc
from pkg_resources import resource_filename


default_config_path = "/etc/onionrouter/"
default_mappings_path = "/etc/onionrouter/mappings"


class OnionRouter(object):
    ref_config = (olib.find_file("/etc/onionrouter/", "onionrouter.ini")
                  or resource_filename("onionrouter",
                                       "configs/onionrouter.ini"))
    rerouters = namedtuple('rerouters', ('lazy', 'onion'))

    def __init__(self, config_path, map_path=None):
        self.config_file = config_handlers.get_conffile(config_path,
                                                        prefix="onionrouter")
        self.mappings_path = map_path
        config_handlers.ConfigIntegrityChecker(
            ref_config=self.ref_config, other_config=self.config_file).verify()
        self.config = config_handlers.config_reader(self.config_file)
        self.rerouters = self.rerouters(
            lazy=routers.LazyPostfixRerouter(self.config, self.mappings_path),
            onion=routers.OnionPostfixRerouter(
                self.config, OnionServiceLookup(self.config)))

    @property
    def myname(self):
        return self.config.get("DOMAIN", "hostname")

    @staticmethod
    def get_domain(name):
        return name.split("@")[1]

    def reroute(self, domain):
        if self.myname == domain:
            return tuple(["200 :"])
        else:
            return (self.rerouters.lazy.reroute(domain)
                    or self.rerouters.onion.reroute(domain))

    def run(self, address):
        try:
            domain = self.get_domain(address)
        except IndexError:
            return "500 Request key is not an email address"
        routing = self.reroute(domain)
        # in the end, there can be only one response
        return routing[0] if routing else "500 Not found"


class OnionRouterRunner(object):

    @staticmethod
    def add_arguments():
        parser = argparse.ArgumentParser(
            description='onionrouter daemon for postifx rerouting')
        parser.add_argument('--interactive', '-i', default=False,
                            action='store_true',
                            help='Simple test route mode without daemon')
        parser.add_argument('--debug', '-d', default=False,
                            action='store_true',
                            help='Debug mode. Run daemon and also print the '
                                 'queries & replies')
        parser.add_argument('--client', '-c', default=False,
                            action='store_true',
                            help='Client mode. Connect as a client to daemon '
                                 'for testing / debug')
        parser.add_argument('--config', default=default_config_path,
                            help='Absolute path to config folder/file '
                                 '(default: %(default)s)', type=str)
        parser.add_argument('--mappings', default=default_mappings_path,
                            help='Absolute path to static mappings folder/file'
                                 ' (default: %(default)s)', type=str)
        parser.add_argument('--host', '-l', default="127.0.0.1",
                            help="Host for daemon to listen "
                                 "(default: %(default)s)", type=str)
        parser.add_argument('--port', '-p', default=23000, type=int,
                            help="Port for daemon to listen "
                                 "(default: %(default)s)")
        return parser

    @staticmethod
    def interactive_reroute(onion_router):
        while True:
            addr = olib.cross_input("Enter an email address: ")
            if addr == 'get *':
                print("500 Request key is not an email address")
            else:
                print(onion_router.run(addr))

    @staticmethod
    def reroute_debugger(question, answer):
        print("[Q]: {q}\n"
              "[A]: {a}".format(q=question, a=answer))

    @staticmethod
    def craft_resolver(callback):
        return partial(msockets.resolve, resolve_callback=callback)

    @staticmethod
    def validate_flag_arguments(*flags):
        if len([x for x in flags if x]) > 1:
            raise RuntimeWarning("Cannot use multiple modes. "
                                 "Choose only one mode")

    def main(self):
        args = self.add_arguments().parse_args()
        self.validate_flag_arguments(args.interactive, args.client, args.debug)
        onion_router = OnionRouter(config_path=args.config,
                                   map_path=args.mappings)

        if args.interactive:
            self.interactive_reroute(onion_router)

        if args.client:
            msockets.client(args.host, args.port)
        else:
            resolver = self.craft_resolver(self.reroute_debugger
                                           if args.debug
                                           else lambda *args: args)
            msockets.daemonize_server(onion_router, args.host, args.port,
                                      resolver=resolver)


def main():
    try:
        OnionRouterRunner().main()
    except (exc.ConfigError, socket_error, RuntimeWarning) as err:
        print(err)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()
