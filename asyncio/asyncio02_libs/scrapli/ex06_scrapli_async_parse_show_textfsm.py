from pprint import pprint
import asyncio
from scrapli import AsyncScrapli
from scrapli.exceptions import ScrapliException

r1 = {
    "host": "192.168.100.1",
    "auth_username": "cisco",
    "auth_password": "cisco",
    "auth_secondary": "cisco",
    "auth_strict_key": False,
    "timeout_socket": 5,  # timeout for establishing socket/initial connection in seconds
    "timeout_transport": 10,  # timeout for ssh|telnet transport in seconds
    "platform": "cisco_iosxe",
    "transport": "asyncssh",
}


async def send_show(device, show_commands):
    cmd_dict = {}
    if type(show_commands) == str:
        show_commands = [show_commands]
    try:
        async with AsyncScrapli(**device) as ssh:
            for cmd in show_commands:
                reply = await ssh.send_command(cmd)
                parsed_data = reply.textfsm_parse_output()
                if parsed_data:
                    cmd_dict[cmd] = parsed_data
                else:
                    cmd_dict[cmd] = reply.result
        return cmd_dict
    except ScrapliException as error:
        print(error, device["host"])


if __name__ == "__main__":
    output = asyncio.run(send_show(r1, ["sh run | i ^interface", "show ip int br"]))
    pprint(output)

