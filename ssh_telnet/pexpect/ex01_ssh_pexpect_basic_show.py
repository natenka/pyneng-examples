from pprint import pprint
import pexpect


def cisco_send_show_command(host, username, password, enable_pass, command):
    print(f"Подключаюсь {host}")
    with pexpect.spawn(f"ssh {username}@{host}", encoding="utf-8") as ssh:
        ssh.expect("[Pp]assword")
        ssh.sendline(password)
        ssh.expect(">")
        ssh.sendline("enable")
        ssh.expect("Password")
        ssh.sendline(enable_pass)
        ssh.expect("#")

        ssh.sendline("terminal length 0")
        ssh.expect("#")

        ssh.sendline(command)
        ssh.expect("#")
        output = ssh.before
    return output.replace("\r\n", "\n")


if __name__ == "__main__":
    result = {}
    ip_list = ["192.168.100.1", "192.168.100.2", "192.168.100.3"]
    for ip in ip_list:
        out = cisco_send_show_command(
            ip, "cisco", "cisco", "cisco", "sh ip int br"
        )
        result[ip] = out
    pprint(result)
