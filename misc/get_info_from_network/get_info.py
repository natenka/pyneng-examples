from itertools import repeat
import yaml
import csv
import netmiko
import subprocess
from platform import system as system_name
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

from netmiko import ConnectHandler


def ping_ip(ip):
    param = "-n" if system_name().lower() == "windows" else "-c"
    command = ["ping", param, "3", ip]
    reply = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ip_is_reachable = reply.returncode == 0
    return ip_is_reachable


def ping_ip_addresses(ip_list, limit=5):
    reachable = []
    unreachable = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        results = executor.map(ping_ip, ip_list)
    for ip, status in zip(ip_list, results):
        if status:
            reachable.append(ip)
        else:
            unreachable.append(ip)
    return reachable, unreachable


def dlink_get_hostname_sn(device):
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        output = ssh.send_command("...")

        match_sn = re.search(r"...", output)
        if match_sn:
            sn = match_sn.group(1)
        else:
            sn = None

        prompt = ssh.find_prompt()
        hostname = re.search(r"...", prompt).group(1)
    return (device["host"], hostname, sn)


def cisco_get_hostname_sn(device):
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        output = ssh.send_command("sh version")

        match_sn = re.search(r"Processor board ID (\S+)", output)
        if match_sn:
            sn = match_sn.group(1)
        else:
            sn = None

        prompt = ssh.find_prompt()
        hostname = re.search(r"(\S+)[>#]", prompt).group(1)
    return (device["host"], hostname, sn)


def get_host_sn_write_to_file(devices, filename, limit=10):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_list = []
        for device in devices:
            function = device.pop("function")
            future = executor.submit(function, device)
            future_list.append(future)
        with open(filename, "w") as f:
            wr = csv.writer(f)
            wr.writerow(["vendor", "ip", "hostname", "serial number"])
            for device, f in zip(devices, future_list):
                output = f.result()
                vendor = device["device_type"]
                wr.writerow([vendor, *output])


def collect_info_from_devices(devices_list, output_filename):
    vendor_device_type_map = {
        "Cisco": "cisco_ios",
        "D-LINK": "dlink_ds",
    }
    vendor_function_map = {
        "Cisco": cisco_get_hostname_sn,
        "D-LINK": dlink_get_hostname_sn,
    }
    base_params = {
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
        "timeout": 10,
    }

    devices = [
        {
            **base_params,
            "host": device["ip"],
            "device_type": vendor_device_type_map[device["vendor"]],
            "function": vendor_function_map[device["vendor"]],
        }
        for device in devices_list
    ]
    get_host_sn_write_to_file(devices, output_filename)


def main():
    with open("devices.csv") as f:
        reader = csv.DictReader(f)
        netmiko_support = [
            row for row in reader if row["vendor"] in ("Cisco", "D-LINK")
        ]

    # получаем список IP-адресов и проверяем доступность
    check_ip = [dev["ip"] for dev in netmiko_support]
    reach, unreach = ping_ip_addresses(check_ip)
    print(f"Недоступные адреса:\n{unreach}")

    # Подключение идет только к тем адресам, которые пингуются
    reachable_devices = [dev for dev in netmiko_support if dev["ip"] in reach]
    collect_info_from_devices(reachable_devices, "collected_params_results.csv")


if __name__ == "__main__":
    main()
