from colorama import Fore, init

#Эти две строки не надо вносить внутрь функции,
#так как в таком случае код жутко тормозит
init(autoreset=True)
colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.CYAN, Fore.MAGENTA, Fore.BLUE]


def transform_dict(dictionary, level=0):
    result = ''
    key_template = colors[level]+'    '*(level)+'{}: '
    value_template = colors[level]+'{},\n'
    if type(dictionary) is dict:
        result += Fore.WHITE+'{\n'
        for key, value in dictionary.items():
            result += key_template.format(key)
            result += transform_dict(value, level+1)
    else:
        return value_template.format(dictionary)
    if level == 0:
        return result+'}\n'
    else:
        return result+'},\n'


d = {1000:{10:100, 20:200},
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
    'ip': '10.255.0.101'
    }
}

print(transform_dict(d))
print(transform_dict(london_co))

