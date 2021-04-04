from pprint import pprint
import pexpect
import click
import yaml


def cisco_cfg_device(
    host,
    username,
    password,
    enable_pass,
    cfg_commands,
    check_cmd=None,
    check_str=None,
):
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

        cfg_commands = ["conf t", *cfg_commands, "end"]
        result = ""
        for cmd in cfg_commands:
            ssh.sendline(cmd)
            ssh.expect(["config\S+#", "#"])
            output = ssh.before + ssh.after
            if "%" in output:
                click.secho(
                    f'When executing the command "{cmd}" an error occurred', fg="red"
                )
            result += output.replace("\r\n", "\n")
        if check_cmd and check_str:
            ssh.sendline(check_cmd)
            ssh.expect("#")
            check_output = ssh.before
            if check_str in check_output:
                click.secho("Configuration was successful", fg="green")
            else:
                click.secho("Configuration failed validation", fg="red")
    return result


if __name__ == "__main__":
    cfg_cmds = ["int lo200", "ip address 10.2.2.2 255.255.255.255"]
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
        r1 = devices[0]
        out = cisco_cfg_device(
            **r1,
            cfg_commands=["router ospf 1", "network 0.0.0.0 255.255.255.255 area 0"],
            check_cmd="sh ip ospf",
            check_str="Routing Process",
        )
        pprint(out, width=120)
