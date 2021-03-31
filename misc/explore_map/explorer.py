import re
from pprint import pprint
from queue import Queue

import yaml
from netmiko import (
    ConnectHandler,
    NetMikoAuthenticationException,
    NetMikoTimeoutException,
)


def parse_cdp(output):
    regex = (
        r"IP address: (?P<ip>\S+)\n"
        r".*?"
        r"Interface: (?P<local_port>\S+), +"
        r"Port ID \(outgoing port\): (?P<remote_port>\S+)"
    )

    result = {}

    match_iter = re.finditer(regex, output, re.DOTALL)
    for match in match_iter:
        ip = match.group("ip")
        groupdict = match.groupdict()
        del groupdict["ip"]
        result[ip] = groupdict
    return result


def connect_ssh(params, command, verbose=True):
    if verbose:
        print("Connect...", params)
    try:
        with ConnectHandler(**params) as ssh:
            ssh.enable()
            prompt = ssh.find_prompt()
            return f"{prompt}\n{ssh.send_command(command)}"
    except (NetMikoAuthenticationException, NetMikoTimeoutException) as error:
        print(error)


def topology_bfs(start_device, params):
    visited_hosts = set()
    topology = {}
    q = Queue()
    q.put(start_device)

    while q.qsize() > 0:
        current = q.get()
        params["host"] = current
        if current in visited_hosts:
            continue
        connections = parse_cdp(connect_ssh(params, "sh cdp neig det"))
        topology[current] = connections
        for neighbor, n_data in connections.items():
            if neighbor not in visited_hosts:
                q.put(neighbor)
        visited_hosts.add(current)
    return topology


if __name__ == "__main__":
    common_params = {
        "device_type": "cisco_ios",
        "password": "cisco",
        "secret": "cisco",
        "username": "cisco",
    }
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    start = "192.168.100.1"
    topology = topology_bfs(start, params=common_params)
    pprint(topology)
