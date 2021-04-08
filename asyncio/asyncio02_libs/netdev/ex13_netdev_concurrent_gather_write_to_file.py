from pprint import pprint
import asyncio

import netdev
import yaml


# from ex02_netdev_show.py import send_show
async def send_show(device, commands):
    result = {}
    if type(commands) == str:
        commands = [commands]
    try:
        async with netdev.create(**device) as ssh:
            for cmd in commands:
                output = await ssh.send_command(cmd)
                result[cmd] = output
            return result
    except netdev.exceptions.TimeoutError as error:
        print(error)
    except netdev.exceptions.DisconnectError as error:
        print(error)


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
    with open("devices_netdev.yaml") as f:
        devices = yaml.safe_load(f)
    result = asyncio.run(send_command_to_devices(devices, "sh ip int br"))
    pprint(result, width=120)
