from pprint import pprint
import asyncio

import yaml
from scrapli import AsyncScrapli
from scrapli.exceptions import ScrapliException
import aiofiles


async def send_show(device, show_commands):
    cmd_dict = {}
    if type(show_commands) == str:
        show_commands = [show_commands]
    try:
        async with AsyncScrapli(**device) as ssh:
            for cmd in show_commands:
                reply = await ssh.send_command(cmd)
                cmd_dict[cmd] = reply.result
            prompt = await ssh.get_prompt()
            # тут добавлено приглашение, так как as_completed не сохраняет порядок устройст
            # и таким образом понятно от какого устройства пришел вывод и как называть файл
            return prompt, cmd_dict
    except ScrapliException as error:
        print(error, device["host"])


async def write_to_file(data):
    hostname, command_dict = data
    filename = f"{hostname.lower()}_cmd_output.txt"
    async with aiofiles.open(filename, "w") as f:
        for cmd, output in command_dict.items():
            await f.write(f"\n\n{hostname}{cmd}\n")
            await f.write(output)


async def send_command_to_devices(devices, commands):
    coroutines = [send_show(device, commands) for device in devices]
    tasks = []
    for future in asyncio.as_completed(coroutines):
        result = await future
        tasks.append(asyncio.create_task(write_to_file(result)))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    with open("devices_async.yaml") as f:
        devices = yaml.safe_load(f)
    result = asyncio.run(
        send_command_to_devices(devices, ["sh ip int br", "sh run | i ^router ospf"])
    )
    pprint(result, width=120)
