from platform import system as system_name
import subprocess


def ping_ip_addresses(ip_list):
    param = "-n" if system_name().lower() == "windows" else "-c"
    reachable = []
    unreachable = []
    processes = []
    for ip in ip_list:
        p = subprocess.Popen(
            ["ping", param, "1", ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        processes.append(p)
    for ip, p in zip(ip_list, processes):
        returncode = p.wait()
        if returncode == 0:
            reachable.append(ip)
        else:
            unreachable.append(ip)
    return reachable, unreachable


if __name__ == "__main__":
    unreach_ip = ["10.1.1.1", "10.1.1.2", "10.1.1.3"]
    print(ping_ip_addresses(["8.8.8.8", *unreach_ip]))
