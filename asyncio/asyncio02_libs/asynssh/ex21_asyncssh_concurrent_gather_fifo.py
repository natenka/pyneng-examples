from pprint import pprint
import asyncio

import yaml
import asyncssh

from ex03_asyncssh_show_read_until import read_until, send_show


async def send_command_to_devices(devices, command):
    coroutines = [send_show(**device, command=command) for device in devices]
    result = await asyncio.gather(*coroutines)
    return result


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    result = asyncio.run(send_command_to_devices(devices, "sh ip int br"))
    pprint(result, width=120)
