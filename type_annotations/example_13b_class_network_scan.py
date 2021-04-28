from concurrent.futures import ThreadPoolExecutor
import subprocess
from class_network import Network
from typing import Tuple, List


class ScanNetwork:
    def __init__(self, network: Network) -> None:
        self.network = network

    def _ping_ip(self, ip: str) -> bool:
        result = subprocess.run(f"ping -c 3 {ip}".split(), stdout=subprocess.PIPE)
        if result.returncode == 0:
            return True
        else:
            return False

    def scan(self, max_threads: int = 3) -> Tuple[List[str], List[str]]:
        ok = []
        not_ok = []
        with ThreadPoolExecutor(max_workers=max_threads) as ex:
            results = ex.map(self._ping_ip, self.network.hosts)
            for ip, status in zip(self.network.hosts, results):
                if status:
                    ok.append(ip)
                else:
                    not_ok.append(ip)
        return ok, not_ok


if __name__ == "__main__":
    net1 = Network("192.168.100.0", 29)
    print(net1.hosts)
    # ['192.168.100.1', '192.168.100.2', '192.168.100.3', '192.168.100.4',
    # '192.168.100.5', '192.168.100.6']

    s = ScanNetwork(net1)
    ok, n_ok = s.scan()
    print(ok)
    print(n_ok)
