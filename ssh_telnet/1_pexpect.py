import pexpect
from getpass import getpass


def send_command_cisco(ip, username, password, enable, commands):
    with pexpect.spawn(f"ssh {username}@{ip}") as ssh:
        ssh.expect("Password")
        ssh.sendline(password)
        ssh.expect(">")

        ssh.sendline("enable")
        ssh.expect("Password")

        ssh.sendline(enable)
        ssh.expect("#")

        ssh.sendline("terminal length 0")
        ssh.expect("#")

        result = []
        for command in commands:
            ssh.sendline(command)
            returncode = ssh.expect(["#", pexpect.TIMEOUT, pexpect.EOF])
            if returncode == 0:
                output = ssh.before.decode("utf-8")
                result.append(output)
            else:
                print("Возникла ошибка")
        return result


if __name__ == "__main__":
    command = ["sh clock", "sh ip int br", "sh ip arp"]
    username = input("Введите имя пользователя: ")
    password = getpass()
    enable = getpass("Введи пароль режима enable" )
    ip_list = ["192.168.100.1", "192.168.100.2", "192.168.100.3"]
    for ip in ip_list:
        print(send_command_cisco(ip, username, password, enable, command))
