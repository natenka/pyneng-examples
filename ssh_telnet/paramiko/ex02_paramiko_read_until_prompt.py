import time
from pprint import pprint
import socket
import re

import paramiko
import yaml


def _read_until_prompt(ssh, prompt, pause=0.2, max_read=60000):
    command_output = ""
    ssh.settimeout(5)
    while True:
        try:
            time.sleep(pause)
            part = ssh.recv(max_read).decode("utf-8")
            command_output += part
            if prompt in part:
                break
        except socket.timeout:
            break
    return command_output.replace("\r\n", "\n")


def send_show_commands(
    host, username, password, enable_pass, commands, max_read=60000, pause=0.5
):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
            hostname=host,
            username=username,
            password=password,
            look_for_keys=False,
            allow_agent=False,
            timeout=10,
        )
    except socket.timeout:
        print(f"Failed to connect to {host}")
        return
    except paramiko.SSHException as error:
        print(f"{error} on {host}")
        return

    with client.invoke_shell() as ssh:
        ssh.settimeout(2)

        ssh.send("enable\n")
        ssh.send(f"{enable_pass}\n")
        time.sleep(pause)
        ssh.recv(max_read)
        ssh.send(f"terminal length 0\n")
        time.sleep(pause)
        read_output = ssh.recv(max_read).decode("utf-8")
        match_prompt = re.search(r"\S+#", read_output)

        if match_prompt:
            prompt = match_prompt.group()
        else:
            prompt = "#"

        if type(commands) == str:
            commands = [commands]
        result = {}
        for cmd in commands:
            ssh.send(f"{cmd}\n")
            output = _read_until_prompt(ssh, prompt)
            result[cmd] = output
        return result


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
        for device in devices:
            out = send_show_commands(**device, commands="sh ip int br")
            pprint(out, width=120)
