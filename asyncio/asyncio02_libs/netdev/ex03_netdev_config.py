from pprint import pprint
import asyncio

import netdev
import yaml


r1 = {
    "device_type": "cisco_ios",
    "host": "192.168.100.1",
    "username": "cisco",
    "password": "cisco",
    "secret": "cisco",
}


async def send_cfg(device, cfg_commands):
    if type(cfg_commands) == str:
        cfg_commands = [cfg_commands]
    try:
        async with netdev.create(**device) as ssh:
            output = await ssh.send_config_set(cfg_commands)
            return output
    except netdev.exceptions.TimeoutError as error:
        print(error)
    except netdev.exceptions.DisconnectError as error:
        print(error)


if __name__ == "__main__":
    output_cfg = asyncio.run(
        send_cfg(r1, ["interface lo11", "ip address 11.1.1.1 255.255.255.255"])
    )
    print(output_cfg)
