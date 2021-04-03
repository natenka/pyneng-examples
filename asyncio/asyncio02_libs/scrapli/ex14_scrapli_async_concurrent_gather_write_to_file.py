from pprint import pprint
import asyncio

import yaml
from scrapli import AsyncScrapli
from scrapli.exceptions import ScrapliException


# from ex04_scrapli_async_send_show_commands import send_show
async def send_show(device, show_commands):
    cmd_dict = {}
    if type(show_commands) == str:
        show_commands = [show_commands]
    try:
        async with AsyncScrapli(**device) as ssh:
            for cmd in show_commands:
                reply = await ssh.send_command(cmd)
                cmd_dict[cmd] = reply.result
        return cmd_dict
    except ScrapliException as error:
        print(error, device["host"])


def write_to_file(host, command_dict):
    filename = f"{host.lower().replace('.', '_')}_cmd_output.txt"
    with open(filename, "w") as f:
        for cmd, output in command_dict.items():
            f.write(f"\n\n{host}{cmd}\n")
            f.write(output)


async def send_command_to_devices(devices, commands):
    coroutines = [send_show(device, commands) for device in devices]
    result = await asyncio.gather(*coroutines)
    for dev, output in zip(devices, result):
        write_to_file(dev["host"], output)
    return result


if __name__ == "__main__":
    with open("devices_async.yaml") as f:
        devices = yaml.safe_load(f)
    result = asyncio.run(send_command_to_devices(devices, "sh ip int br"))
    pprint(result, width=120)
