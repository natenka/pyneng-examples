import paramiko
import time
import socket


def send_command(host, username, password, enable, command,
                 wait_for_command=5, prompt="#"):
    MAX_READ = 5000
    SHORT_PAUSE = 0.5
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, look_for_keys=False)
    with client.invoke_shell() as ssh:
        ssh.send('enable\n')
        ssh.send(f'{enable}\n')
        time.sleep(SHORT_PAUSE)
        ssh.send('terminal length 0\n')
        time.sleep(SHORT_PAUSE)
        ssh.recv(MAX_READ)
        ssh.send(f"{command}\n")
        ssh.settimeout(wait_for_command)
        output = ""
        while True:
            try:
                part = ssh.recv(100).decode("utf-8")
                output += part
                # print(part)
                if prompt in output:
                    # print("Found prompt!")
                    break
            except socket.timeout:
                break
        return output


if __name__ == "__main__":
    print(send_command("192.168.100.1", "cisco", "cisco", "cisco",
                       "ping 8.8.8.8 repeat 10", prompt="R1#"))
