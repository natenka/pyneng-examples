import time
from pprint import pprint
import socket
import re

import paramiko
import yaml


class ConnectSSH:
    def __init__(
        self, host, username, password, enable_pass, max_read=60000, read_pause=0.5
    ):
        self.host = host
        self.username = username
        self.password = password
        self.max_read = max_read
        self.read_pause = read_pause

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(
            hostname=host,
            username=username,
            password=password,
            look_for_keys=False,
            allow_agent=False,
            timeout=10,
        )

        self._ssh = client.invoke_shell()
        self._ssh.settimeout(2)

        self._ssh.send("enable\n")
        self._ssh.send(f"{enable_pass}\n")
        time.sleep(read_pause)
        self._ssh.recv(max_read)
        self._ssh.send(f"terminal length 0\n")
        time.sleep(read_pause)
        read_output = self._ssh.recv(max_read).decode("utf-8")
        match_prompt = re.search(r"\S+#", read_output)

        if match_prompt:
            self.prompt = match_prompt.group()
        else:
            self.prompt = "#"

    def _read_until(self, expect_line):
        command_output = ""
        self._ssh.settimeout(5)
        while True:
            try:
                time.sleep(self.read_pause)
                part = self._ssh.recv(self.max_read).decode("utf-8")
                command_output += part
                match_prompt = re.search(f"{expect_line}|{self.prompt}", command_output)
                if match_prompt:
                    break
            except socket.timeout:
                break
        return command_output.replace("\r\n", "\n")

    def _read_until_prompt(self):
        return self._read_until(self.prompt)

    def _read_until_cfg_prompt(self):
        hostname = self.prompt.split("#")[0]
        cfg_regex = rf"{hostname}\(.+\)#"
        return self._read_until(cfg_regex)

    def send_command(self, command):
        self._ssh.send(f"{command}\n")
        result = self._read_until_prompt()
        return result

    def send_config_commands(self, commands):
        cfg_output = ""
        if type(commands) == str:
            commands = ["conf t", commands, "end"]
        else:
            commands = ["conf t", *commands, "end"]
        for cmd in commands:
            self._ssh.send(f"{cmd}\n")
            cfg_output += self._read_until_cfg_prompt()
        return cfg_output

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._ssh.close()

    def close(self):
        self._ssh.close()


if __name__ == "__main__":
    config_commands = ["logging buffered 20010", "ip http server"]

    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
        r1 = devices[0]
        with ConnectSSH(**r1) as r1_ssh:
            out = r1_ssh.send_config_commands(config_commands)
            pprint(out, width=120)
