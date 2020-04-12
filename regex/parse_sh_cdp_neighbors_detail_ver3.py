import re
from pprint import pprint


cdp = {}

regex = (
    r"Device ID: (?P<device>\S+)" # имя устройства
    r"|IP address: (?P<ip>\S+)"
    r"|Platform: (?P<platform>.+),"
    r"|Interface: (?P<port1>\S+), +Port ID \(outgoing port\): (?P<port2>\S+)"
    r"|Cisco IOS Software, (?P<ios>.+),"
)

with open('sh_cdp_neighbors_sw1.txt') as f:
    for line in f:
        match = re.search(regex, line)
        if match:
            last = match.lastgroup
            value = match.group(last)
            print(f"Lastgroup = {last:10}, {value}")
            if last == "device":
                device = value
                cdp[device] = {}
            elif last == "port2":
                cdp[device]["port1"] = match.group("port1")
                cdp[device][last] = value
            else:
                cdp[device][last] = value


pprint(cdp)
