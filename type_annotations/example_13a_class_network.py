import ipaddress
from typing import Tuple, List


class Network:
    all_allocated_ip: List[str] = []

    def __init__(self, network: str, mask: int) -> None:
        self.network = network
        self.mask = mask
        self.allocated: List[str] = []
        ipv4net = ipaddress.ip_network(f"{self.network}/{self.mask}")
        self.hosts = [str(ip) for ip in ipv4net.hosts()]

    def allocate_ip(self, ip: str) -> None:
        if ip in self.hosts:
            if ip not in self.allocated:
                self.allocated.append(ip)
                # Network.all_allocated_ip.append(ip)
                type(self).all_allocated_ip.append(ip)
            else:
                raise ValueError(
                    f"IP-адрес {ip} уже находится в allocated "
                    f"\n{self.allocated}"
                )
        else:
            raise ValueError(
                f"IP-адрес {ip} не входит в сеть "
                f"{self.network}/{self.mask}"
            )

    def __str__(self) -> str:
        print("Вызываю __str__")
        return f"{self.network}/{self.mask}"

    def __repr__(self) -> str:
        print("Вызываю __repr__")
        return f"Network('{self.network}', {self.mask})"

    def __len__(self) -> int:
        print("Вызываю __len__")
        return len(self.hosts)

    def __getitem__(self, index: int) -> str:
        print(f"Вызываю __getitem__ index {index}")
        return self.hosts[index]
