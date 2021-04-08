from pprint import pprint
import asyncio

import yaml

from ex03_asyncssh_show_read_until import send_show


async def connect_ssh_with_semaphore(semaphore, function, *args, **kwargs):
    async with semaphore:
        return await function(*args, **kwargs)


async def send_command_to_devices(devices, command, max_workers=50):
    semaphore = asyncio.Semaphore(max_workers)
    coroutines = [
        connect_ssh_with_semaphore(semaphore, send_show, **device, command=command)
        for device in devices
    ]
    result = await asyncio.gather(*coroutines)
    return result


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    result = asyncio.run(send_command_to_devices(devices, "sh ip int br"))
    pprint(result, width=120)
