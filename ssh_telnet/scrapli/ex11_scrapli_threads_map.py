from concurrent.futures import ThreadPoolExecutor
from pprint import pprint
from itertools import repeat
import logging

import yaml
from scrapli import Scrapli
from scrapli.exceptions import ScrapliException


logging.getLogger("scrapli").setLevel(logging.WARNING)

logging.basicConfig(
    format="%(threadName)s %(name)s %(levelname)s: %(message)s", level=logging.INFO
)


def send_show(device, show_commands):
    host = device["host"]
    if type(show_commands) == str:
        show_commands = [show_commands]
    cmd_dict = {}
    logging.info(f">>> Connecting to {host}")
    try:
        with Scrapli(**device) as ssh:
            for cmd in show_commands:
                reply = ssh.send_command(cmd)
                cmd_dict[cmd] = reply.result
        logging.info(f"<<< Received output from {host}")
        return cmd_dict
    except ScrapliException as error:
        print(error, host)


def send_show_to_devices(devices, show, max_threads=10):
    result_dict = {}
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        results = executor.map(send_show, devices, repeat(show))
        for dev, output in zip(devices, results):
            result_dict[dev["host"]] = output
    return result_dict


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    output = send_show_to_devices(devices, "sh int desc")
    pprint(output, width=120)
