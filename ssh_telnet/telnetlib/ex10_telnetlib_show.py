import time
import telnetlib
from pprint import pprint


def to_bytes(line):
    return f"{line}\n".encode("utf-8")


def cisco_send_show_command(host, username, password, enable_pass, command):
    with telnetlib.Telnet(host) as conn:
        conn.read_until(b"Username")
        conn.write(to_bytes(username))
        conn.read_until(b"Password")
        conn.write(to_bytes(password))

        idx, _, _ = conn.expect([b">", b"#"])
        if idx == 0:
            conn.write(b"enable\n")
            conn.read_until(b"Password")
            conn.write(to_bytes(password))
            conn.read_until(b"#")
        conn.write(b"terminal length 0\n")
        conn.read_until(b"#")

        conn.write(to_bytes(command))
        output = conn.read_until(b"#").decode("utf-8")
        return output


if __name__ == "__main__":
    result = {}
    ip_list = ["192.168.100.1", "192.168.100.2", "192.168.100.3"]
    for ip in ip_list:
        out = cisco_send_show_command(
            ip, "cisco", "cisco", "cisco", "sh ip int br"
        )
        result[ip] = out
    pprint(result, width=120)
