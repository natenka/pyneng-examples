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


async def send_cfg(device, cfg_commands, strict=False):
    output = ""
    if type(cfg_commands) == str:
        cfg_commands = [cfg_commands]
    try:
        async with AsyncScrapli(**device) as ssh:
            reply = await ssh.send_configs(cfg_commands, stop_on_failed=strict)
            for cmd_reply in reply:
                if cmd_reply.failed:
                    print(f"При выполнении команды возникла ошибка:\n{reply.result}\n")
            output = reply.result
        return output
    except ScrapliException as error:
        print(error, device["host"])


if __name__ == "__main__":
    output_cfg = asyncio.run(
        send_cfg(
            r1, ["interface lo11", "ip address 11.1.1.1 255.255.255.255"], strict=True
        )
    )
    print(output_cfg)
