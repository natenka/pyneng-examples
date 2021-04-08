from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from pprint import pprint

import yaml

from ex02_paramiko_read_until_prompt import send_show_commands


def send_show_to_devices(devices, show, max_threads=10):
    result_dict = {}
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_list = [executor.submit(send_show_commands, **dev, commands=show)
                   for dev in devices]
        for dev, future in zip(devices, future_list):
            result_dict[dev["host"]] = future.result()
    return result_dict


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    output = send_show_to_devices(devices, "sh int desc")
    pprint(output, width=120)
