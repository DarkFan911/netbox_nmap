#!/usr/bin/env python3

import logging
import sys

from configparser import ConfigParser
from argparse import ArgumentParser
from os.path import expanduser, isfile
from datetime import datetime
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

from nbs import NetBoxScanner

argument = str(sys.argv[1])

if argument == 'nmap':
    from nbs.nmap import Nmap

local_config = expanduser('~/.netbox-scanner.conf')
global_config = '/opt/netbox-4.1.7/netbox-scanner.conf'
config = ConfigParser()

if isfile(local_config):
    config.read(local_config)
elif isfile(global_config):
    config.read(global_config)
else:
    raise FileNotFoundError('Configuration file was not found.')

netbox = config['NETBOX']
if argument == 'nmap':
    nmap = config['NMAP']

parser = ArgumentParser(description='netbox-scanner')
subparsers = parser.add_subparsers(title='Commands', dest='command')
subparsers.required = True
if argument == 'nmap':
    argsp = subparsers.add_parser('nmap', help='Nmap module')
args = parser.parse_args()

logfile = '{}/netbox-scanner-{}.log'.format(
    netbox['logs'],
    datetime.now().isoformat()
)
logging.basicConfig(
    filename=logfile,
    level=logging.INFO,
    format='%(asctime)s\tnetbox-scanner\t%(levelname)s\t%(message)s'
)
logging.getLogger().addHandler(logging.StreamHandler())

# useful if you have tls_verify set to no
disable_warnings(InsecureRequestWarning)


def cmd_nmap(s):  # nmap handler
    h = Nmap(nmap['path'], nmap['unknown'])
    h.run()
    scanner.sync(h.hosts)


if __name__ == '__main__':
    scanner = NetBoxScanner(
        netbox['address'],
        netbox['token'],
        netbox['tls_verify'],
        nmap['tag'],
        nmap.getboolean('cleanup')
   )

    if args.command == 'nmap':
        cmd_nmap(scanner)

    exit(0)
