from pprint import pprint
from scrapli import Scrapli

r1 = {
    "host": "192.168.100.1",
    "auth_username": "cisco",
    "auth_password": "cisco",
    "auth_secondary": "cisco",
    "auth_strict_key": False,
    "platform": "cisco_iosxe",
    "channel_log": True,  # channel_log in scrapli_channel.log
}


def send_show(device, show_commands):
    if type(show_commands) == str:
        show_commands = [show_commands]
    cmd_dict = {}
    with Scrapli(**r1) as ssh:
        for cmd in show_commands:
            reply = ssh.send_command(cmd)
            cmd_dict[cmd] = reply.result
    return cmd_dict


if __name__ == "__main__":
    print("show".center(20, "#"))
    output = send_show(r1, ["sh ip int br", "sh ver | i uptime"])
    pprint(output, width=120)
