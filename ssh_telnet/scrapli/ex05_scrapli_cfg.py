from pprint import pprint
from scrapli import Scrapli

r1 = {
    "host": "192.168.100.1",
    "auth_username": "cisco",
    "auth_password": "cisco",
    "auth_secondary": "cisco",
    "auth_strict_key": False,
    "platform": "cisco_iosxe",
}


def send_cfg(device, cfg_commands, strict=False):
    output = ""
    if type(cfg_commands) == str:
        cfg_commands = [cfg_commands]
    with Scrapli(**r1) as ssh:
        reply = ssh.send_configs(cfg_commands, stop_on_failed=strict)
        for cmd_reply in reply:
            # cmd_reply.raise_for_status()
            if cmd_reply.failed:
                print(f"При выполнении команды возникла ошибка:\n{reply.result}\n")
        output = reply.result
    return output


if __name__ == "__main__":
    output_cfg = send_cfg(
        r1, ["interfacelo11", "ip address 11.1.1.1 255.255.255.255"], strict=True
    )
    print(output_cfg)
