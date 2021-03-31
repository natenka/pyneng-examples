from pprint import pprint
import pexpect
import re


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

        output = ""
        ssh.sendline(command)

        while True:
            print("### page")
            match = ssh.expect(["#", "--More--", pexpect.TIMEOUT], timeout=5)
            page = ssh.before
            page = re.sub(r" +\x08+ +\x08+", "\n", page)
            output += page
            if match == 0:
                break
            elif match == 1:
                ssh.send(" ")
            else:
                print(">>> Timeout")
                break
    return output.replace("\r\n", "\n")


if __name__ == "__main__":
    ip_list = ["192.168.100.1", "192.168.100.2", "192.168.100.3"]
    out = cisco_send_show_command(
        ip_list[0], "cisco", "cisco", "cisco", "sh run"
    )
    with open("result_r1.txt", "w") as f:
        f.write(out)
