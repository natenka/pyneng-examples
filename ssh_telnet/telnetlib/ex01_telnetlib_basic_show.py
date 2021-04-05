import time
import telnetlib
from pprint import pprint

import yaml


def to_bytes(line):
    return f"{line}\n".encode("utf-8")


def send_show_command(host, username, password, enable_pass, command):
    with telnetlib.Telnet(host) as conn:
        conn.read_until(b"Username")
        conn.write(to_bytes(username))
        conn.read_until(b"Password")
        conn.write(to_bytes(password))

        idx, *trash = conn.expect([b">", b"#"])
        if idx == 0:
            conn.write(b"enable\n")
            conn.read_until(b"Password")
            conn.write(to_bytes(password))
            conn.read_until(b"#")
        conn.write(b"terminal length 0\n")
        conn.read_until(b"#")

        conn.write(to_bytes(command))
        output = conn.read_until(b"#").decode("utf-8")
        return output.replace("\r\n", "\n")


if __name__ == "__main__":
    with open("devices_telnetlib.yaml") as f:
        devices = yaml.safe_load(f)
        for device in devices:
            out = send_show_command(**device, command="sh ip int br")
            pprint(out, width=120)
