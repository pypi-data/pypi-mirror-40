ip_tools
I have written my own python ip/subnet tool. Its python2/3. I use theese methods to conver ip mask formats and to check if ip/subnet belong to other subnet. Perhaps these are not the best, but they get the job done.

Instalation:

pip install iptoolsjj
Example:

from iptoolsjj import *
Check if 192.168.10.10 is inside 192.168.10.0/22:

if IP_TOOLS().is_in_subnet("192.168.10.10", "192.168.10.0/22"):
    print ("yes")
Convert mask '255.255.255.240' to '28':

print(IP_TOOLS().mask255_to_dec("255.255.255.240"))
Convert mask '28' to '['255', '255', '255', '240']' (normally it's list format):

print(IP_TOOLS().dec_to_mask255(28))
or

print(".".join(IP_TOOLS().dec_to_mask255(28)))
