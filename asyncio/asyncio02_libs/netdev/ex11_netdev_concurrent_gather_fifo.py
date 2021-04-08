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



async def send_command_to_devices(devices, commands):
    coroutines = [send_show(device, commands) for device in devices]
    result = await asyncio.gather(*coroutines)
    return result


if __name__ == "__main__":
    with open("devices_netdev.yaml") as f:
        devices = yaml.safe_load(f)
    result = asyncio.run(send_command_to_devices(devices, "sh ip int br"))
    pprint(result, width=120)
