import time
import telnetlib
from pprint import pprint
import socket
import logging

import yaml


logging.getLogger("paramiko").setLevel(logging.WARNING)

logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s: %(message)s", level=logging.INFO
)


def to_bytes(line):
    return f"{line}\n".encode("utf-8")


def send_show_commands(host, username, password, enable_pass, commands, timeout=10):
    try:
        with telnetlib.Telnet(host, timeout=timeout) as conn:
            try:
                login_output = conn.read_until(b"Username")
                conn.write(to_bytes(username))
                login_output += conn.read_until(b"Password")
                conn.write(to_bytes(password))
                idx, *trash = conn.expect([b">", b"#"])
            except socket.timeout as error:
                logging.warning(f"authentication error on {host}")
                time.sleep(0.5)
                login_output += conn.read_very_eager()
                logging.debug(login_output.decode("utf-8"))
                return

            if idx == 0:
                conn.write(b"enable\n")
                conn.read_until(b"Password")
                conn.write(to_bytes(password))
                conn.read_until(b"#")
            conn.write(b"terminal length 0\n")
            conn.read_until(b"#")

            result_dict = {}
            if type(commands) == str:
                commands = [commands]
            for cmd in commands:
                conn.write(to_bytes(cmd))
                output = conn.read_until(b"#").decode("utf-8")
                result_dict[cmd] = output.replace("\r\n", "\n")
            return result_dict

    except socket.timeout as error:
        logging.warning(f"{error} on {host}")


if __name__ == "__main__":
    with open("devices_telnetlib.yaml") as f:
        devices = yaml.safe_load(f)
        for device in devices:
            out = send_show_commands(**device, commands="sh ip int br")
            pprint(out, width=120)
