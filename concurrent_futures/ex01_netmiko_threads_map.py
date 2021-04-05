from concurrent.futures import ThreadPoolExecutor
import re
from pprint import pprint
import time
import random
from itertools import repeat
from datetime import datetime
import logging
import netmiko
import yaml


logging.getLogger("paramiko").setLevel(logging.WARNING)
logging.getLogger("netmiko").setLevel(logging.WARNING)

logging.basicConfig(
    format="%(threadName)s %(name)s %(levelname)s: %(message)s", level=logging.INFO
)


def send_show(device, commands):
    result = {}
    if type(commands) == str:
        commands = [commands]
    try:
        with netmiko.Netmiko(**device) as ssh:
            ssh.enable()
            for cmd in commands:
                output = ssh.send_command(cmd)
                result[cmd] = output
            return result
    except netmiko.NetmikoTimeoutException as error:
        print(f"Failed to connect to {device['host']}")
    except paramiko.ssh_exception.AuthenticationException:
        print(f"Authentication error on {device['host']}")


def send_show_to_devices(devices, show, workers=10):
    result_dict = {}
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = executor.map(send_show, devices, repeat(show))
        for dev, output in zip(devices, results):
            result_dict[dev["host"]] = output
    return result_dict


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    results = send_show_to_devices(devices, "sh int desc")
    pprint(results, width=120)
