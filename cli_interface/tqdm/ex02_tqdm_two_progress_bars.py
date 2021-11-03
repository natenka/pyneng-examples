from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from pprint import pprint

from scrapli import Scrapli
from scrapli.exceptions import ScrapliException
import tqdm
import yaml


logging.getLogger("scrapli").setLevel(logging.WARNING)
logging.basicConfig(
    filename="log_ex02.log",
    format="{asctime} {threadName} {name} {levelname} {message}",
    style="{",
    level=logging.DEBUG,
)


def conn_ssh_threads(devices, command, limit=3):
    result_dict = {}

    with ThreadPoolExecutor(max_workers=limit) as executor:
        futures = [executor.submit(send_show, device, command) for device in devices]

        success_bar = tqdm.tqdm(total=len(devices), desc="Correct".rjust(10))
        futures = tqdm.tqdm(futures, total=len(devices), desc="All".rjust(10))
        for device, task in zip(devices, futures):
            host = device["host"]
            command_output = task.result()
            if command_output:
                success_bar.update(1)
            result_dict[host] = command_output
    return result_dict


def send_show(device, show_command):
    try:
        with Scrapli(**device) as ssh:
            reply = ssh.send_command(show_command)
            return reply.result
    except ScrapliException as error:
        logging.info(f"Error {error} on {device['host']}")


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    results = conn_ssh_threads(devices * 4, "sh clock")
    pprint(results)
