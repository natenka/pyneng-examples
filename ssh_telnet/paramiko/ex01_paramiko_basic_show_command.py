import paramiko
import time
from pprint import pprint


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
    ip_list = ["192.168.100.1", "192.168.100.2", "192.168.100.3"]
    for ip in ip_list:
        out = send_show_command(ip, "cisco", "cisco", "cisco", "sh ip int br")
        pprint(out, width=120)
