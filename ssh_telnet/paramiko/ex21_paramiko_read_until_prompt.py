import paramiko
import time
from pprint import pprint
import socket
import re


def cisco_send_show_command(
    host, username, password, enable_pass, command, max_read=60000,
    pause=0.5,
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
        ssh.settimeout(2)

        ssh.send("enable\n")
        ssh.send(f"{enable_pass}\n")
        time.sleep(pause)
        ssh.recv(max_read)
        ssh.send(f"terminal length 0\n")
        time.sleep(pause)
        read_output = ssh.recv(max_read).decode("utf-8")
        prompt = re.search(r"\S+#", read_output).group()

        ssh.send(f"{command}\n")
        output = ""
        ssh.settimeout(5)
        while True:
            try:
                time.sleep(pause)
                part = ssh.recv(max_read).decode("utf-8")
                output += part
                if prompt in part:
                    break
            except socket.timeout:
                break
        return output


if __name__ == "__main__":
    result = {}
    ip_list = ["192.168.100.1", "192.168.100.2", "192.168.100.3"]
    for ip in ip_list:
        out = cisco_send_show_command(
            ip, "cisco", "cisco", "cisco", "sh ip int br"
        )
        result[ip] = out
        break
    pprint(result)
