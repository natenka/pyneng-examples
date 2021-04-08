from pprint import pprint
import asyncio
import asyncssh

import yaml
from ex11_asyncssh_basic_class import ConnectAsyncSSH


async def send_show(device, command):
    host = device["host"]
    try:
        async with ConnectAsyncSSH(**device) as ssh:
            output = await ssh.send_show_command("sh ip int br")
            return output
    except asyncio.TimeoutError:
        print(f"Connection Timeout on {host}")
    except asyncssh.PermissionDenied:
        print(f"Authentication Error on {host}")
    except asyncssh.Error as error:
        print(f"{error} on {host}")


async def send_command_to_devices(devices, command):
    coroutines = [send_show(device, command) for device in devices]
    result = await asyncio.gather(*coroutines)
    return result


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    result = asyncio.run(send_command_to_devices(devices, "sh ip int br"))
    pprint(result, width=120)
