import telnetlib
import time
from pprint import pprint
import re

import yaml


def to_bytes(line):
    return f"{line}\n".encode("utf-8")


def send_show_command(host, username, password, enable_pass, command):
    with telnetlib.Telnet(host) as telnet:
        telnet.read_until(b"Username")
        telnet.write(to_bytes(username))
        telnet.read_until(b"Password")
        telnet.write(to_bytes(password))
        index, m, output = telnet.expect([b">", b"#"])
        if index == 0:
            telnet.write(b"enable\n")
            telnet.read_until(b"Password")
            telnet.write(to_bytes(enable_pass))
            telnet.read_until(b"#", timeout=5)

        telnet.write(to_bytes(command))
        result = ""

        while True:
            index, match, output = telnet.expect([b"--More--", b"#"], timeout=5)
            output = output.decode("utf-8")
            output = re.sub(" +--More--| +\x08+ +\x08+", "\n", output)
            result += output
            if index in (1, -1):
                break
            telnet.write(b" ")

        return result.replace("\r\n", "\n")


if __name__ == "__main__":
    with open("devices_telnetlib.yaml") as f:
        devices = yaml.safe_load(f)
        for device in devices:
            out = send_show_command(**device, command="sh run")
            pprint(out, width=120)
