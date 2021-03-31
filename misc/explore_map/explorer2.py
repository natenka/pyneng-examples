import re
from pprint import pprint

import yaml
from netmiko import (
    ConnectHandler,
    NetMikoAuthenticationException,
    NetMikoTimeoutException,
)


def parse_cdp(output):
    regex = (
        r"Device ID: (?P<host>\w+)\."
        r".*?"
        r"IP address: (?P<ip>\S+)\n"
        r".*?"
        r"Interface: (?P<local_port>\S+), +"
        r"Port ID \(outgoing port\): (?P<remote_port>\S+)"
    )

    neighbors = {}

    match_iter = re.finditer(regex, output, re.DOTALL)
    for match in match_iter:
        hostname = match.group("host")
        groupdict = match.groupdict()
        del groupdict["host"]
        neighbors[hostname] = groupdict
    return neighbors


def connect_ssh(params, command, verbose=True):
    if verbose:
        print("Connect...", params)
    try:
        with ConnectHandler(**params) as ssh:
            ssh.enable()
            prompt = ssh.find_prompt()
            hostname = re.search(r"(\S+)[>#]", prompt).group(1)
            return hostname, ssh.send_command(command)
    except (NetMikoAuthenticationException, NetMikoTimeoutException) as error:
        print(error)


def explore_topology(start_device_ip, params):
    visited_hostnames = set()
    visited_ipadresses = set()
    topology = {}
    todo = []
    todo.append(start_device_ip)

    while len(todo) > 0:
        current_ip = todo.pop(0)
        params["host"] = current_ip

        current_host, sh_cdp_neighbors_output = connect_ssh(params, "sh cdp neig det")
        neighbors = parse_cdp(sh_cdp_neighbors_output)

        topology[current_host] = neighbors
        visited_ipadresses.add(current_ip)
        visited_hostnames.add(current_host)

        for neighbor, n_data in neighbors.items():
            neighbor_ip = n_data["ip"]
            if (
                neighbor not in visited_hostnames
                and neighbor_ip not in visited_ipadresses
                and neighbor_ip not in todo
            ):
                todo.append(neighbor_ip)
    return topology


if __name__ == "__main__":
    common_params = {
        "device_type": "cisco_ios",
        "password": "cisco",
        "secret": "cisco",
        "username": "cisco",
        "timeout": 4
    }
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    start = "192.168.100.1"
    topology = explore_topology(start, params=common_params)
    pprint(topology)
