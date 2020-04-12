print('__init__')



from .ssh import * #relative
from cisco_connect.telnet import CiscoTelnet #absolut

a = 10

__all__ = [ssh.__all__ + telnet.__all__]
