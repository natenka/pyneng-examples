from concurrent.futures import ThreadPoolExecutor
import re
from pprint import pprint
from itertools import repeat
import logging

import netmiko
import paramiko
import yaml


logging.getLogger("paramiko").setLevel(logging.WARNING)
logging.getLogger("netmiko").setLevel(logging.WARNING)

logging.basicConfig(
    format="%(threadName)s %(name)s %(levelname)s: %(message)s", level=logging.INFO
)


def send_show_command(device, show):
    host = device["host"]
    logging.info(f">>> Connecting to {host}")
    try:
        with netmiko.Netmiko(**device) as ssh:
            ssh.enable()
            output = ssh.send_command(show)
            logging.debug(f"\n{output}\n")
            logging.info(f"<<< Received output from {host}")
            return output
    except netmiko.NetmikoTimeoutException as error:
        logging.info(f"Failed to connect to {host}")
    except paramiko.ssh_exception.AuthenticationException:
        logging.info(f"Authentication error on {host}")


def send_show_to_devices(devices, show, max_threads=10):
    result_dict = {}
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        results = executor.map(send_show_command, devices, repeat(show))
        for dev, output in zip(devices, results):
            result_dict[dev["host"]] = output
    return result_dict


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    r = send_show_to_devices(devices, "sh int desc")
    pprint(r, width=120)
