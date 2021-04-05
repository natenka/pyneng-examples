from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
import logging
from pprint import pprint
import socket

import yaml

from ex11_telnetlib_basic_class import CiscoTelnet


logging.basicConfig(
    format="%(threadName)s %(name)s %(levelname)s: %(message)s", level=logging.INFO
)


def send_show_command(device, command):
    host = device["host"]
    logging.info(f">>> Connecting to {host}")
    try:
        with CiscoTelnet(**device) as ssh:
            output = ssh.send_command(command)
            return output
        logging.info(f"<<< Received output from {host}")
    except socket.timeout:
        print(f"Failed to connect to {host}")


def send_show_to_devices(devices, show, max_threads=10):
    result_dict = {}
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        results = executor.map(send_show_command, devices, repeat(show))
        for dev, output in zip(devices, results):
            result_dict[dev["host"]] = output
    return result_dict


if __name__ == "__main__":
    with open("devices_telnetlib.yaml") as f:
        devices = yaml.safe_load(f)
    output = send_show_to_devices(devices, "sh int desc")
    pprint(output, width=120)
