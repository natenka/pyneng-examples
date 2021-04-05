from platform import system as system_name
import subprocess


def ping_ip(ip_address):
    """
    Ping IP address and return:
    True on success:
    False on failure:
    """
    param = "-n" if system_name().lower() == "windows" else "-c"
    command = ["ping", param, "1", ip_address]
    reply = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ip_is_reachable = reply.returncode == 0
    return ip_is_reachable


def ping_ip_addresses(ip_list):
    reachable = []
    unreachable = []
    for ip in ip_list:
        if ping_ip(ip):
            reachable.append(ip)
        else:
            unreachable.append(ip)
    return reachable, unreachable


if __name__ == "__main__":
    unreach_ip = ["10.1.1.1", "10.1.1.2", "10.1.1.3"]
    print(ping_ip_addresses(["8.8.8.8", *unreach_ip]))
