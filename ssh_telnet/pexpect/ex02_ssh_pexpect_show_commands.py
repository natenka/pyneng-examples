from pprint import pprint
import pexpect


def cisco_send_show_commands(host, username, password, enable_pass, commands):
    print(f"Подключаюсь {host}")
    with pexpect.spawn(f"ssh {username}@{host}", encoding="utf-8") as ssh:
        ssh.expect("[Pp]assword")
        ssh.sendline(password)
        ssh.expect(">")
        ssh.sendline("enable")
        ssh.expect("Password")
        ssh.sendline(enable_pass)
        ssh.expect("\S+#")
        prompt = ssh.after

        ssh.sendline("terminal length 0")
        ssh.expect(prompt)

        result = {}
        if type(commands) == str:
            commands = [commands]
        for cmd in commands:
            ssh.sendline(cmd)
            ssh.expect("\r\n")
            ssh.expect(prompt)
            output = ssh.before
            result[cmd] = output.replace("\r\n", "\n")
    return result


if __name__ == "__main__":
    ip_list = ["192.168.100.1", "192.168.100.2", "192.168.100.3"]
    for ip in ip_list:
        out = cisco_send_show_commands(
            ip, "cisco", "cisco", "cisco", ["sh clock", "sh int desc"]
        )
        pprint(out)

