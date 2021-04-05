import subprocess
from concurrent.futures import ThreadPoolExecutor


class ScanNetwork:
    def __init__(self, ip_list):
        self.ip_list = ip_list

    @staticmethod
    def _ping_ip(ip):
        result = subprocess.run(
            ["ping", "-c", "3", "-n", ip], stdout=subprocess.DEVNULL
        )
        ip_is_reachable = result.returncode == 0
        return ip_is_reachable

    def scan(self, limit=3):
        reachable = []
        unreachable = []
        with ThreadPoolExecutor(max_workers=limit) as executor:
            results = executor.map(self._ping_ip, self.ip_list)
        for ip, status in zip(self.ip_list, results):
            if status:
                reachable.append(ip)
            else:
                unreachable.append(ip)
        return reachable, unreachable


if __name__ == "__main__":
    scanner = ScanNetwork(["8.8.8.8", "192.168.100.22", "192.168.100.1"])
    print(scanner.scan())
