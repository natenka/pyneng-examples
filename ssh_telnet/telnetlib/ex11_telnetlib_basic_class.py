import telnetlib
import time
from pprint import pprint
import socket
import re

import yaml


class CiscoTelnet:
    def __init__(
        self, host, username, password, enable_pass, encoding="utf-8", timeout=10
    ):
        self.host = host
        self.username = username
        self.password = password
        self.enable_pass = enable_pass
        self.encoding = encoding

        self.telnet = telnetlib.Telnet(host, timeout=timeout)
        self.telnet.read_until(b"Username:")
        self._write_line(username)
        self.telnet.read_until(b"Password:")
        self._write_line(password)

        idx, *trash = self.telnet.expect([b">", b"#"])
        if idx == 0:
            self._write_line("enable")
            self.telnet.read_until(b"Password")
            self._write_line(enable_pass)
            self.telnet.read_until(b"#")

        self._write_line("terminal length 0")
        self.telnet.read_until(b"#")

    def _write_line(self, line):
        self.telnet.write(line.encode(self.encoding) + b"\n")

    def _read_until_prompt(self):
        output = self.telnet.read_until(b"#").decode(self.encoding)
        return output.replace("\r\n", "\n")

    def send_command(self, command):
        self._write_line(command)
        return self._read_until_prompt()

    def send_config_commands(self, commands):
        cfg_output = ""
        if type(commands) == str:
            commands = ["conf t", commands, "end"]
        else:
            commands = ["conf t", *commands, "end"]
        for cmd in commands:
            self._write_line(cmd)
            cfg_output += self._read_until_prompt()
        return cfg_output

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.telnet.close()

    def close(self):
        self.telnet.close()


if __name__ == "__main__":
    config_commands = ["logging buffered 20010", "ip http server"]

    with open("devices_telnetlib.yaml") as f:
        devices = yaml.safe_load(f)
        r1 = devices[0]
        with CiscoTelnet(**r1) as r1_ssh:
            out_show = r1_ssh.send_command("sh ip int br")
            pprint(out_show, width=120)

            out = r1_ssh.send_config_commands(config_commands)
            pprint(out, width=120)
