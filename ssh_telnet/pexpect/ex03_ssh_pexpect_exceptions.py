from pprint import pprint
import pexpect


def cisco_send_show_commands(host, username, password, enable_pass, commands):
    print(f"Подключаюсь {host}")
    try:
        with pexpect.spawn(f"ssh {username}@{host}", timeout=10, encoding="utf-8") as ssh:
            ssh.expect("[Pp]assword")
            ssh.sendline(password)
            enable_mode = ssh.expect([">", "#"])
            if enable_mode == 0:
                ssh.sendline("enable")
                ssh.expect("Password")
                ssh.sendline(enable_pass)
                ssh.expect("#")

            ssh.sendline("terminal length 0")
            ssh.expect("\S+#")
            prompt = ssh.after

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
    except pexpect.exceptions.TIMEOUT as error:
        print(f"Устройство {host} не доступно")


if __name__ == "__main__":
    ip_list = ["192.168.100.1", "192.168.100.2", "192.168.100.3"]
    for ip in ip_list:
        if ip == "192.168.100.1":
            password = "sdfsdf"
        else:
            password = "cisco"
        out = cisco_send_show_commands(
            ip, "cisco", password, "cisco", ["sh clock", "sh int desc"]
        )
        pprint(out)

