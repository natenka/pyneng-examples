from pprint import pprint
import socket

import yaml
from netmiko import (
    Netmiko,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


def send_show_command(device, commands):
    result = {}
    if type(commands) == str:
        commands = [commands]
    try:
        with Netmiko(**device) as ssh:
            ssh.enable()
            for command in commands:
                output = ssh.send_command(command)
                result[command] = output
        return result
    except NetmikoAuthenticationException as error:
        print(error)
    except socket.timeout:
        print(f"Timeout when connecting to {device['host']}")


if __name__ == "__main__":
    device = {
        "device_type": "cisco_ios_telnet",
        "host": "192.168.100.1",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }
    result = send_show_command(device, ["sh clock", "sh ip int br"])
    pprint(result, width=120)
