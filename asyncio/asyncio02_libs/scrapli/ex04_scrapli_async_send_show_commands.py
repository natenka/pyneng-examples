import asyncio
from scrapli import AsyncScrapli
from scrapli.exceptions import ScrapliException

r1 = {
    "host": "192.168.139.1",
    "auth_username": "cisco",
    "auth_password": "cisco",
    "auth_secondary": "cisco",
    "auth_strict_key": False,
    "timeout_socket": 5,  # timeout for establishing socket/initial connection in seconds
    "timeout_transport": 10,  # timeout for ssh|telnet transport in seconds
    "platform": "cisco_iosxe",
    "transport": "asyncssh",
    "transport_options": {
        "asyncssh": {
            "encryption_algs": ["aes256-cbc", "aes192-cbc"],
            "kex_algs": ["diffie-hellman-group14-sha1", "diffie-hellman-group1-sha1"],
        }
    },
}


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


if __name__ == "__main__":
    output = asyncio.run(send_show(r1, "show ip int br"))
    print(output)
