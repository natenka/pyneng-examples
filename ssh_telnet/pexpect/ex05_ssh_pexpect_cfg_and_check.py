from pprint import pprint
import pexpect
import click


def cisco_cfg_device(
    host, username, password, enable_pass,
    cfg_commands, check_cmd=None, check_str=None,
):
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
        #ssh.expect("\S+config\S+#")
        ssh.expect("#")
        result = ssh.before + ssh.after
        for cmd in cfg_commands:
            ssh.sendline(cmd)
            ssh.expect("#")
            output = ssh.before + ssh.after
            if "%" in output:
                click.secho(
                    f"При выполнении команды {cmd} возникла ошибка", fg="red"
                )
                # print(output)
            result += output.replace("\r\n", "\n")
        ssh.sendline("end")
        ssh.expect("#")
        result += ssh.before + ssh.after
        if check_cmd and check_str:
            ssh.sendline(check_cmd)
            ssh.expect("#")
            check_output = ssh.before
            if check_str in check_output:
                click.secho("Настройка прошла успешно", fg="green")
            else:
                click.secho("Настройка не прошла проверку", fg="red")
    return result


if __name__ == "__main__":
    ip_list = ["192.168.100.1", "192.168.100.2", "192.168.100.3"]
    for ip in ip_list:
        out = cisco_cfg_device(
            ip, "cisco", "cisco", "cisco",
            ["router ospf 1", "network 0.0.0.0 255.255.255.255 area 0"],
            check_cmd="sh ip ospf", check_str="Routing Process"
        )
        pprint(out)
        break

