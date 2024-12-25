import pynetbox

NETBOX_URL = 'x.x.x.x'
NETBOX_TOKEN = 'Token'

netbox = pynetbox.api(url=NETBOX_URL, token=NETBOX_TOKEN)

ip_addresses = netbox.ipam.ip_addresses.all()

for ip in ip_addresses:
print(f"IP Address: {ip.address}, Description: {ip.description}")
