from pprint import pprint
import pexpect


def cisco_cfg_device(host, username, password, enable_pass, cfg_commands):
    print(f"Подключаюсь {host}")
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
        ssh.expect("#")

        ssh.sendline("conf t")
        ssh.expect("config\S+#")
        result = ""
        for cmd in cfg_commands:
            ssh.sendline(cmd)
            ssh.expect("config\S+#")
            output = ssh.before
            if "%" in output:
                print(f"При выполнении команды {cmd} возникла ошибка")
                print(output)
            result += output.replace("\r\n", "\n")
        ssh.sendline("end")
        ssh.expect("#")
    return result


if __name__ == "__main__":
    ip_list = ["192.168.100.1", "192.168.100.2", "192.168.100.3"]
    for ip in ip_list:
        out = cisco_cfg_device(
            ip, "cisco", "cisco", "cisco",
            ["int lo200", "ip address 10.2.2.2 255.255.255.255"]
        )
        pprint(out)
        break

