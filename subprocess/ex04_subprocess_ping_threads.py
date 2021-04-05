from platform import system as system_name
import subprocess
from concurrent.futures import ThreadPoolExecutor


def ping_ip(ip):
    param = "-n" if system_name().lower() == "windows" else "-c"
    command = ["ping", param, "1", ip]
    reply = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ip_is_reachable = reply.returncode == 0
    return ip_is_reachable


def ping_ip_addresses(ip_list, max_workers=10):
    reachable = []
    unreachable = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(ping_ip, ip_list)
    for ip, status in zip(ip_list, results):
        if status:
            reachable.append(ip)
        else:
            unreachable.append(ip)
    return reachable, unreachable


if __name__ == "__main__":
    unreach_ip = ["10.1.1.1", "10.1.1.2", "10.1.1.3"]
    print(ping_ip_addresses(["8.8.8.8", *unreach_ip]))
