import ipaddress


class Network:
    def __init__(self, network):
        self.network = network
        net = ipaddress.ip_network(network)
        self.hosts = [str(ip) for ip in net.hosts()]

    def __iter__(self):
        print("вызываю __iter__")
        return iter(self.hosts)

