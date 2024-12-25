import os
import xml.etree.ElementTree as ET
import json

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
                # Проверяем, доступны ли имена хостов
                hostname_element = host.find('hostnames')
                if hostname_element is not None and hostname_element.find('hostname') is not None:
                    hostname = hostname_element.find('hostname').attrib['name']
                else:
                    hostname = self.unknown

                # Создаем словарь и добавляем его в список
                host_info = {
                    'address': address,
                    'hostname': hostname
                }
                self.hosts.append(json.dumps(host_info))  # Преобразуем в JSON и добавляем в список

        # Пример вывода в консоль
        for host_json in self.hosts:
            print(host_json)  # Каждый хост в формате JSON
