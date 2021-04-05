from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
import logging
from pprint import pprint
import socket

import paramiko
import yaml

from ex23_paramiko_basic_class import ConnectSSH


logging.getLogger("paramiko").setLevel(logging.WARNING)

logging.basicConfig(
    format="%(threadName)s %(name)s %(levelname)s: %(message)s", level=logging.INFO
)


def send_show_command(device, command):
    host = device["host"]
    logging.info(f">>> Connecting to {host}")
    try:
        with ConnectSSH(**device) as ssh:
            output = ssh.send_command(command)
            return output
        logging.info(f"<<< Received output from {host}")
    except socket.timeout:
        logging.info(f"Failed to connect to {host}")
    except paramiko.SSHException as error:
        logging.info(f"{error} on {host}")


def send_show_to_devices(devices, show, max_threads=10):
    result_dict = {}
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        results = executor.map(send_show_command, devices, repeat(show))
        for dev, output in zip(devices, results):
            result_dict[dev["host"]] = output
    return result_dict


if __name__ == "__main__":
    with open("devices_paramiko.yaml") as f:
        devices = yaml.safe_load(f)
    output = send_show_to_devices(devices, "sh int desc")
    pprint(output, width=120)
