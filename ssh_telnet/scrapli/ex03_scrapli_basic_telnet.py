from scrapli.driver.core import IOSXEDriver

r1 = {
    "host": "192.168.100.1",
    "auth_username": "cisco",
    "auth_password": "cisco",
    "auth_secondary": "cisco",
    "auth_strict_key": False,
    "transport": "telnet",
    "port": 23,  # обязательно указывать при подключении telnet
}


def send_show(device, show_command):
    with IOSXEDriver(**r1) as ssh:
        reply = ssh.send_command(show_command)
        return reply.result


def send_cfg(device, cfg_commands):
    with IOSXEDriver(**r1) as ssh:
        reply = ssh.send_configs(cfg_commands)
        return reply.result


if __name__ == "__main__":
    output = send_show(r1, "sh ip int br")
    print(output)

    output_cfg = send_cfg(r1, ["interface lo11", "ip address 11.1.1.1 255.255.255.255"])
    print(output_cfg)
