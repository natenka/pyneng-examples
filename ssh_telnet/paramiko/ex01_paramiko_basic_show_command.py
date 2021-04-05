import time
from pprint import pprint

import paramiko
import yaml


def send_show_command(
    host, username, password, enable_pass, command, max_read=60000, pause=0.5
):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=host,
        username=username,
        password=password,
        look_for_keys=False,
        allow_agent=False,
    )
    with client.invoke_shell() as ssh:
        ssh.settimeout(5)
        ssh.send("enable\n")
        ssh.send(f"{enable_pass}\n")
        time.sleep(pause)
        ssh.send(f"terminal length 0\n")
        time.sleep(pause)
        ssh.recv(max_read)

        ssh.send(f"{command}\n")
        time.sleep(pause)
        output = ssh.recv(max_read)
        return output.decode("utf-8").replace("\r\n", "\n")


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
        for device in devices:
            out = send_show_command(**device, command="sh ip int br")
            pprint(out, width=120)
