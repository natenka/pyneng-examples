import time
import socket
from pprint import pprint
import re

import yaml
import paramiko


def send_show_command(
    host, username, password, enable_pass, command, max_read=60000, pause=0.5
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
        ssh.send("enable\n")
        ssh.send(f"{enable_pass}\n")
        time.sleep(pause)
        read_output = ssh.recv(max_read).decode("utf-8")
        match_prompt = re.search(r"\S+#", read_output)

        if match_prompt:
            prompt = match_prompt.group()
        else:
            prompt = "#"

        result = {}
        ssh.send(f"{command}\n")
        ssh.settimeout(5)

        output = ""
        while True:
            try:
                page = ssh.recv(max_read).decode("utf-8")
                output += page
                time.sleep(0.2)
            except socket.timeout:
                break
            if "More" in page:
                ssh.send(" ")
        output = re.sub(" +--More--| +\x08+ +\x08+", "\n", output)

        return output.replace("\r\n", "\n")


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
        r1 = devices[0]
        out = send_show_command(**r1, command="sh run")
        pprint(out, width=120)
