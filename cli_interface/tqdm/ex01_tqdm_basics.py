from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint

from scrapli import Scrapli
from scrapli.exceptions import ScrapliException
import tqdm
import yaml


def conn_ssh_threads(devices, command, limit=3, progress_bar=True):
    result_dict = {}
    with ThreadPoolExecutor(max_workers=limit) as executor:
        futures = [executor.submit(send_show, device, command) for device in devices]
        if progress_bar:
            futures = tqdm.tqdm(futures, total=len(devices))
        for device, task in zip(devices, futures):
            host = device["host"]
            result_dict[host] = task.result()

    return result_dict


def send_show(device, show_command):
    try:
        with Scrapli(**device) as ssh:
            reply = ssh.send_command(show_command)
            return reply.result
    except ScrapliException as error:
        print(error, device["host"])


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    results = conn_ssh_threads(devices * 4, "sh clock")
    pprint(results)
