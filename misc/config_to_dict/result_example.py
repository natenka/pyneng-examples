{
    "hostname Liverpool": [],
    "interface Ethernet0/13.200": {
        " bandwidth 100000": [],
        " encapsulation dot1Q 100": [],
        " xconnect 10.2.2.2 12100 encapsulation mpls": {
            "  backup peer 10.4.4.4 14100": ["   backup delay 1 1"],
            "  ip rsvp bandwidth": [],
        },
    },
    "interface Ethernet0/3.100": {
        " bandwidth 100000": [],
        " encapsulation dot1Q 100": [],
        " ip rsvp bandwidth": [],
        " xconnect 10.2.2.2 12100 encapsulation mpls": {
            "  backup peer 10.4.4.4 14100": ["   backup delay 1 1"]
        },
    },
    "interface GigabitEthernet0/0": [" description WAN to Liverpool sw1 G0/1"],
    "interface GigabitEthernet0/0.1111": [
        " description MPLS to LONDON",
        " encapsulation dot1Q 1111",
        " ip address 10.11.1.2 255.255.255.252",
        " ip ospf network point-to-point",
        " ip ospf hello-interval 1",
        " ip ospf cost 10",
    ],
    "interface GigabitEthernet0/1": [" description LAN Liverpool to sw1 G0/2"],
    "interface GigabitEthernet0/1.1550": {
        " bandwidth 100000": [],
        " description PW BS Liverpool - LONDON": [],
        " encapsulation dot1Q 1550": [],
        " ip rsvp bandwidth": [],
        " xconnect 10.10.1.1 11111 encapsulation mpls": [
            "  backup peer 10.10.1.2 11121",
            "  backup delay 1 1",
        ],
    },
    "interface GigabitEthernet0/1.791": {
        " description PW IT Liverpool - LONDON": [],
        " encapsulation dot1Q 791": [],
        " xconnect 10.10.1.1 1111 encapsulation mpls": [
            "  backup peer 10.10.1.2 1121",
            "  backup delay 1 1",
        ],
    },
    "interface Loopback10": [
        " description MPLS loopback",
        " ip address 10.10.11.1 255.255.255.255",
    ],
    "router ospf 10": [
        " router-id 10.10.11.1",
        " auto-cost reference-bandwidth 10000",
        " network 10.0.0.0 0.255.255.255 area 0",
    ],
}
