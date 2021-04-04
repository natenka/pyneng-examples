from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint
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
        return {host: cmd_dict}
    except ScrapliException as error:
        print(error, host)


def send_show_to_devices(devices, commands, max_threads=10):
    result_dict = {}
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_list = [
            executor.submit(send_show, dev, commands[dev["host"]]) for dev in devices
        ]
        for f in as_completed(future_list):
            result_dict.update(f.result())
    return result_dict


if __name__ == "__main__":
    ip_command_map = {
        "192.168.100.3": ["sh ip int br", "sh arp"],
        "192.168.100.1": "sh arp",
        "192.168.100.2": ["sh ip int br", "sh int desc"],
    }
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    output = send_show_to_devices(devices, ip_command_map)
    # pprint sorted dict keys
    pprint(output, width=120)
    # real order:
    print(output.keys())
