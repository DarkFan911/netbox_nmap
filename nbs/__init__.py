import os
import xml.etree.ElementTree as ET
import json
import logging
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from pynetbox import api


class Nmap(object):
    def __init__(self, path, unknown):
        self.unknown = unknown
        self.path = path
        self.hosts = list()

    def run(self):
        for f in os.listdir(self.path):
            if not f.endswith('.xml'):
                continue
            abspath = os.path.join(self.path, f)
            tree = ET.parse(abspath)
            root = tree.getroot()

            for host in root.findall('host'):
                address = host.find('address').attrib['addr']
                hostname_element = host.find('hostnames')
                if hostname_element is not None and hostname_element.find('hostname') is not None:
                    hostname = hostname_element.find('hostname').attrib['name']
                else:
                    hostname = self.unknown

                # Добавляем в список хостов как кортеж
                self.hosts.append((address, hostname))  # Используем кортеж

        # Возвращаем список хостов
        return self.hosts


class NetBoxScanner(object):
    def __init__(self, address, token, tls_verify, tag, cleanup):
        self.base_url = f"https://{address}/api/"
        self.session = requests.Session()
        self.token = token
        self.tag = tag
        self.session.verify = False
        self.cleanup = cleanup

        if tls_verify == 'no':
            self.session.verify = False
        else:
            self.session.verify = True

        self.netbox = api(address, token)
        self.netbox.http_session = self.session

        self.stats = {
            'unchanged': 0,
            'created': 0,
            'updated': 0,
            'deleted': 0,
            'errors': 0
        }

        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Token {self.token}'
        }

    def sync_host(self, host):
        try:
            nbhost = self.netbox.ipam.ip_addresses.get(address=host[0])
        except Exception as e:
            logging.error(f"Error retrieving IP {host[0]}: {str(e)}")
            self.stats['errors'] += 1
            return False

        if nbhost:
            if self.tag in nbhost.tags:
                if host[1] != nbhost.description:
                    aux = nbhost.description
                    payload = {'description': host[1]}
                    logging.info(f'PATCH request to update host {host[0]}: {payload}')

                    response = self.session.patch(
                        f"{self.netbox.base_url}/ipam/ip-addresses/{nbhost.id}/",
                        headers=self.headers,
                        json=payload
                    )

                    if response.status_code == 200:
                        logging.info(f'updated: {host[0]} "{aux}" -> "{host[1]}"')
                        self.stats['updated'] += 1
                    else:
                        logging.error(f'Error updating {host[0]}: {response.content}')
                        self.stats['errors'] += 1
                else:
                    logging.info(f'unchanged: {host[0]} "{host[1]}"')
                    self.stats['unchanged'] += 1
            else:
                logging.info(f'unchanged: {host[0]} "{host[1]}"')
                self.stats['unchanged'] += 1
        else:
            payload = {'address': host[0], 'description': host[1]}  # Убедимся, что payload корректный

            logging.info(f'POST request to create host {host[0]}: {payload}')
            response = self.session.post(
                f"{self.netbox.base_url}/ipam/ip-addresses/",
                headers=self.headers,
                json=payload
            )

            if response.status_code == 201:
                logging.info(f'created: {host[0]} "{host[1]}"')
                self.stats['created'] += 1
            else:
                logging.error(f'Error creating {host[0]}: {response.content}')
                self.stats['errors'] += 1

    def sync(self, hosts):
        for s in self.stats:
            self.stats[s] = 0

        logging.info('started: {} hosts'.format(len(hosts)))
        for host in hosts:
            self.sync_host(host)

        if self.cleanup:
            self.garbage_collector(hosts)

    def garbage_collector(self, hosts):
        """Remove unused hosts from NetBox."""
        all_hosts = self.netbox.ipam.ip_addresses.all()
        managed_hosts = {host[0] for host in hosts}  # Хосты, которые должны остаться

        for nbhost in all_hosts:
            if nbhost.address not in managed_hosts and self.tag in nbhost.tags:
                response = self.session.delete(
                    f"{self.base_url}/ipam/ip-addresses/{nbhost.id}/",
                    headers=self.headers
                )
                if response.status_code == 204:
                    logging.info(f'Deleted: {nbhost.address}')
                    self.stats['deleted'] += 1
                else:
                    logging.error(f'Error deleting {nbhost.address}: {response.content}')
                    self.stats['errors'] += 1

        logging.info('finished: .{} +{} ~{} -{} !{}'.format(
            self.stats['unchanged'],
            self.stats['created'],
            self.stats['updated'],
            self.stats['deleted'],
            self.stats['errors']
        ))

        return True

# Пример использования
nmap_path = './'
unknown_host = 'unknown-host'
netbox_address = 'https://x.x.x.x'
netbox_token = 'token'
tls_verify = 'no'
tag = 'sync-tag'
cleanup = True

nmap_scanner = Nmap(nmap_path, unknown_host)
netbox_scanner = NetBoxScanner(netbox_address, netbox_token, tls_verify, tag, cleanup)

# Получаем данные из Nmap
hosts = nmap_scanner.run()

# Синхронизируем данные с NetBox
netbox_scanner.sync(hosts)
