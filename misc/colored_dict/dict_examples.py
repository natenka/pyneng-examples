int_d = {1000:{10:100, 20:200},
         2000:{10:100, 20:200},
         3000:{10:100, 20:200},
         4000:{100:{200:2, 300:3}}}


london_co = {
    'r1' : {
    'hostname': 'london_r1',
    'location': '21 New Globe Walk',
    'vendor': 'Cisco',
    'model': '4451',
    'ios': '15.4',
    'ip': {'fa0/0':'10.255.0.1',
           'fa0/1':'10.255.1.1',
           'fa0/2':'10.255.2.1'}
    },
    'r2' : {
    'hostname': 'london_r2',
    'location': '21 New Globe Walk',
    'vendor': 'Cisco',
    'model': '4451',
    'ios': '15.4',
    'ip': {'fa0/0':'10.255.11.1',
           'fa0/1':'10.255.12.1',
           'fa0/2':'10.255.13.1'}
    },
    'sw1' : {
    'hostname': 'london_sw1',
    'location': '21 New Globe Walk',
    'vendor': 'Cisco',
    'model': '3850',
    'ios': '3.6.XE',
    'ip': ['10.255.0.101', '10.255.2.101']
    }
}


playbook = [{'gather_facts': False,
  'hosts': 'cisco-routers',
  'name': 'Run show commands on routers',
  'tasks': [{'name': 'run sh ip int br', 'raw': 'sh ip int br | ex unass'},
            {'name': 'run sh ip route', 'raw': 'sh ip route'}]},
 {'gather_facts': False,
  'hosts': 'cisco-switches',
  'name': 'Run show commands on switches',
  'tasks': [{'name': 'run sh int status', 'raw': 'sh int status'},
            {'name': 'run sh vlan', 'raw': 'show vlan'}]}]

list_of_tuples = [('Interface', 'IP', 'Status', 'Protocol'),
 ('FastEthernet0/0', '15.0.15.1', 'up', 'up'),
 ('FastEthernet0/1', '10.0.12.1', 'up', 'up'),
 ('FastEthernet0/2', '10.0.13.1', 'up', 'up'),
 ('Loopback0', '10.1.1.1', 'up', 'up'),
 ('Loopback100', '100.0.0.1', 'up', 'up')]
